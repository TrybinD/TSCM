
import numpy as np

from src.data.problem import Problem
from src.data.solution import Solution
from src.solvers.base_solver import BaseSolver


class RandomSolver(BaseSolver):

    def solve(self, problem: Problem) -> Solution:
        operations = list(problem.operations_matrix.columns)

        solution = {}

        for operation in operations:
            operation_solution = {}
            sub_operations_to_be_done = list(problem.operations_matrix[problem.operations_matrix[operation]==1].index)
            for sub_operation in sub_operations_to_be_done:
                available_cities = problem.costs_matrix.columns[problem.costs_matrix.loc[sub_operation] < float("inf")]
                operation_solution[sub_operation] = np.random.choice(available_cities)

            solution[operation] = operation_solution


        return solution
