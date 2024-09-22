
import numpy as np

from src.data.problem import Problem
from src.data.solution import Solution
from src.solvers.base_solver import BaseSolver


class DPSolver(BaseSolver):

    def solve(self, problem: Problem) -> Solution:
        
        solution = {}

        operations = list(problem.operations_matrix.columns)
        cities = list(problem.distances_matrix.index)

        ls_matrix = problem.distances_matrix.values * problem.distances_coef
        os_matrix = (problem.costs_matrix.values * problem.times_matrix.values) / problem.productivity.values

        os_matrix[os_matrix==np.inf] = 2**32
        ls_matrix[ls_matrix==np.inf] = 2**32

        for operation in operations:

            costs = {}
            next_cities = {}

            sub_operations_mask = (problem.operations_matrix[operation]==1).values

            sub_operations = list(problem.operations_matrix[sub_operations_mask].index)

            os_matrix_masked = os_matrix[sub_operations_mask]

            i = len(sub_operations) - 1

            for m, city in enumerate(cities):
                costs[(sub_operations[i], city)] = os_matrix_masked[i, m]

            while i > 0:
                i -= 1

                for m, city in enumerate(cities):
                     
                    next_m_costs = [os_matrix_masked[i, m] + ls_matrix[m, next_m] + costs[(sub_operations[i+1], next_city)]
                                    for next_m, next_city in enumerate(cities)]
                    
                    costs[(sub_operations[i], city)] = min(next_m_costs)

                    next_cities[(sub_operations[i], city)] = cities[np.argmin(next_m_costs)]

            operation_solution = {}

            prev_city = None

            for sub_operation in sub_operations:

                if prev_city is None:
                    prev_city = min([(city, costs[(sub_operation, city)]) for city in cities], key=lambda x: x[1])[0]
                    operation_solution[sub_operation] = prev_city
                    prev_sub_operation = sub_operation
                else:
                    prev_city = next_cities[(prev_sub_operation, prev_city)]
                    operation_solution[sub_operation] = prev_city
                    prev_sub_operation = sub_operation

            solution[operation] = operation_solution

        return solution
                    





                 


