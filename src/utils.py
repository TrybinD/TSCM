


from src.data.problem import Problem
from src.data.solution import Solution


def calculate_costs(problem: Problem, solution: Solution):
    cost = 0

    for operation, operation_path in solution.items():
        sub_operations_to_be_done = set(problem.operations_matrix[problem.operations_matrix[operation]==1].index)
        prev_city = None
        for sub_operation, city in operation_path.items():
            sub_operations_to_be_done.remove(sub_operation)
            # operation cost
            cost += problem.costs_matrix.loc[sub_operation, city] * problem.times_matrix.loc[sub_operation, city] / problem.productivity[city]

            # logistic cost
            if prev_city is not None:
                cost += problem.distances_coef * problem.distances_matrix.loc[prev_city, city]

            if cost == float("inf"):
                raise ValueError(f"Unavailable operation for {operation}: sub-operation {sub_operation} in city {city}")

            prev_city = city

        if sub_operations_to_be_done:
            raise ValueError(f"Not all sub_operation done for {operation}: {sub_operations_to_be_done}")
        
    return cost