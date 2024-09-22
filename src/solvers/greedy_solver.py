


from src.data.problem import Problem
from src.data.solution import Solution
from src.solvers.base_solver import BaseSolver


class GreedySolver(BaseSolver):

    def solve(self, problem: Problem) -> Solution:
        operations = list(problem.operations_matrix.columns)
        cities = list(problem.distances_matrix.index)

        solution = {}

        for operation in operations:
            operation_solution = {}

            sub_operations_to_be_done = list(problem.operations_matrix[problem.operations_matrix[operation]==1].index)

            cur_city = None

            for sub_operation in sub_operations_to_be_done:

                possable_costs = {}

                for city in cities:
                    city_cost = 0

                    # operation cost
                    city_cost += problem.costs_matrix.loc[sub_operation, city] * problem.times_matrix.loc[sub_operation, city] / problem.productivity[city]

                    # logistic cost
                    if cur_city is not None:
                        city_cost += problem.distances_coef * problem.distances_matrix.loc[cur_city, city]

                    possable_costs[city] = city_cost

                operation_solution[sub_operation] = min(possable_costs, key=possable_costs.get)

            solution[operation] = operation_solution

        return solution