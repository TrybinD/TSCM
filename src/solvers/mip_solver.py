from mip import Model, xsum, BINARY
import numpy as np


from src.data.problem import Problem
from src.data.solution import Solution
from src.solvers.base_solver import BaseSolver


class PaperMIPSolver(BaseSolver):
    def __init__(self, max_time: float = float("inf")):
        self.max_time = max_time

    def solve(self, problem: Problem) -> Solution:
        operations = list(problem.operations_matrix.columns)
        cities = list(problem.distances_matrix.index)
        sub_operations = list(problem.operations_matrix.index)

        operations_matrix = problem.operations_matrix.to_numpy(copy=True)
        ls_matrix = problem.distances_matrix.values * problem.distances_coef
        os_matrix = (problem.costs_matrix.values * problem.times_matrix.values) / problem.productivity.values

        os_matrix[os_matrix==np.inf] = 2**32
        ls_matrix[ls_matrix==np.inf] = 2**32

        model = Model()

        model.verbose = False

        gamma = model.add_var_tensor(shape=(len(sub_operations), len(operations), len(cities)),
                                     name="gamma", 
                                     var_type=BINARY)

        delta = model.add_var_tensor(shape=(len(cities), len(cities), len(sub_operations)-1, len(operations)),
                                     name="delta", 
                                     var_type=BINARY)
        
        model.objective = (xsum(os_matrix[i, m]*gamma[i, k, m] for i in range(len(sub_operations)) for m in range(len(cities))for k in range(len(operations))) 
                           + xsum(ls_matrix[m, m_s]*delta[m, m_s, i, k] for k in range(len(operations)) for i in range(len(sub_operations)-1) for m in range(len(cities)) for m_s in range(len(cities))))
        
        
        for i in range(len(sub_operations)):
            for k in range(len(operations)):
                model += (xsum(gamma[i, k, m] for m in range(len(cities))) == operations_matrix[i, k])

        for i in range(len(sub_operations)-1):
            for k in range(len(operations)):
                i_add = 1
                while i + i_add < len(operations_matrix) and operations_matrix[i + i_add, k] != 1:
                    i_add += 1
                if i + i_add == len(operations_matrix):
                    continue
                for m in range(len(cities)):
                    for m_s in range(len(cities)):
                        model += (gamma[i, k, m] + gamma[i+i_add, k, m_s] - 1 <= delta[m, m_s, i, k])


        model.optimize(max_seconds=self.max_time)

        res = [(operation, sub_operation, city) 
               for k, operation in enumerate(operations) 
               for i, sub_operation in enumerate(sub_operations) 
               for m, city in enumerate(cities) if gamma[i, k, m].x >= 0.99]
        
        solution = {}

        for operation, sub_operation, city in res:
            if operation not in solution:
                solution[operation] = {sub_operation: city}
            else:
                solution[operation][sub_operation] = city


        return solution


class MIPSolver(BaseSolver):
    def __init__(self, max_time: float = float("inf")):
        self.max_time = max_time
    
    def solve(self, problem: Problem) -> Solution:

        solution = {}

        operations = list(problem.operations_matrix.columns)
        cities = list(problem.distances_matrix.index)

        ls_matrix = problem.distances_matrix.values * problem.distances_coef
        os_matrix = (problem.costs_matrix.values * problem.times_matrix.values) / problem.productivity.values

        os_matrix[os_matrix==np.inf] = 2**32
        ls_matrix[ls_matrix==np.inf] = 2**32

        for operation in operations:

            sub_operations_mask = (problem.operations_matrix[operation]==1).values

            sub_operations = list(problem.operations_matrix[sub_operations_mask].index)

            os_matrix_masked = os_matrix[sub_operations_mask]

            model = Model()

            model.verbose = False

            gamma = model.add_var_tensor(shape=(len(sub_operations), len(cities)),
                                         name="gamma",
                                         var_type=BINARY)
            
            delta = model.add_var_tensor(shape=(len(cities), len(cities), len(sub_operations)-1),
                                         name="delta", 
                                         var_type=BINARY)
            
            model.objective = (xsum(os_matrix_masked[i, m]*gamma[i, m] for i in range(len(sub_operations)) for m in range(len(cities))) 
                               + xsum(ls_matrix[m, m_s]*delta[m, m_s, i] for i in range(len(sub_operations)-1) for m in range(len(cities)) for m_s in range(len(cities))))
            
            for i in range(len(sub_operations)):
                model += (xsum(gamma[i, m] for m in range(len(cities))) == 1)

            for i in range(len(sub_operations)-1):
                for m in range(len(cities)):
                    for m_s in range(len(cities)):
                        model += (gamma[i, m] + gamma[i+1, m_s] - 1 <= delta[m, m_s, i])

            model.optimize(max_seconds=self.max_time)

            res = [(sub_operation, city) 
                    for i, sub_operation in enumerate(sub_operations) 
                    for m, city in enumerate(cities) if gamma[i, m].x > 0]
            
            operation_solution = {}

            for sub_operation, city in res:
                operation_solution[sub_operation] = city

            solution[operation] = operation_solution


        return solution
    
                


            




            
            

            










