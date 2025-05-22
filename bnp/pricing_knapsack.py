from typing import List

from pyscipopt import Model


def pricing_solver(sizes: List[int], capacity: int, dual_solution: dict[float], together: set[tuple[int, int]],
                   apart: set[tuple[int, int]]) -> tuple[float, List[int]]:
    """
    Solve the pricing problem for the knapsack problem (with branching constraints)

    Parameters:
    sizes: List[int] - the sizes of the items
    capacity: int - the capacity of the knapsack
    dual_solution: dict[float] - the dual solution of the linear relaxation
    together: set[tuple[int]] - the pairs of items that must be together
    apart: set[tuple[int]] - the pairs of items that must be apart

    Returns:
    tuple[float, List[int]] - the minimum reduced cost and the packing of the items
    """

    profits = [dual_solution[i] for i in range(len(sizes))]
    if len(together) > 0 or len(apart) > 0:
        result = solve_knapsack_with_constraints(sizes, profits, capacity, together, apart)
    else:
        result = solve_knapsack(sizes, profits, capacity)

    min_red_cost = 1 - result[0]

    return min_red_cost, result[1]


def solve_knapsack(sizes: List[int], values: List[float], capacity: int) -> tuple[float, List[int]]:
    """
    Solve the knapsack problem

    Parameters:
    sizes: List[int] - the sizes of the items
    values: List[float] - the values of the items
    capacity: int - the capacity of the knapsack

    Returns:
    tuple[float, List[int]] - the optimal value and the packing of the items
    """

    model = Model("Knapsack")
    n = len(sizes)
    
    # Decision variables
    x = {}
    for i in range(n):
        x[i] = model.addVar(vtype="B", name=f"x_{i}")
    
    # Capacity Constraint
    model.addCons(sum(sizes[i] * x[i] for i in range(n)) <= capacity)

    # Objective: maximize the value
    model.setObjective(sum(values[i] * x[i] for i in range(n)), "maximize")

    model.optimize()

    # Construct the solution
    selected = []
    for i in range(n):
        if model.getVal(x[i]) > 0.5:
            selected.append(i)

    return model.getObjVal(), selected

    #raise NotImplementedError("The knapsack solver is not implemented yet")


def solve_knapsack_with_constraints(
        sizes: List[int], values: List[float], capacity: int, together: set[tuple[int, int]],
        apart: set[tuple[int, int]]
) -> tuple[float, List[int]]:
    """
    Solve the knapsack problem with branching constraints

    Parameters:
    sizes: List[int] - the sizes of the items
    values: List[float] - the values of the items
    capacity: int - the capacity of the knapsack
    together: set[tuple[int]] - the pairs of items that must be together
    apart: set[tuple[int]] - the pairs of items that must be apart

    Returns:
    tuple[float, List[int]] - the optimal value and the packing of the items
    """

    model = Model("Knapsack with constraints")
    n = len(sizes)
    x = {i: model.addVar(vtype="B", name=f"x_{i}") for i in range(n)}

    # Capacity constraint
    model.addCons(sum(sizes[i] * x[i] for i in range(n)) <= capacity)

    # Together constraints: x_i - x_j == 0
    for i, j in together:
        model.addCons(x[i] - x[j] == 0, name=f"together_{i}_{j}")

    # Apart constraints: x_i + x_j <= 1
    for i, j in apart:
        model.addCons(x[i] + x[j] <= 1, name=f"apart_{i}_{j}")

    # Objective: maximize the value
    # Objective: maximize value
    model.setObjective(sum(values[i] * x[i] for i in range(n)), "maximize")

    model.optimize()

    selected = [i for i in range(n) if model.getVal(x[i]) > 0.5]
    return model.getObjVal(), selected
    raise NotImplementedError("The knapsack solver with constraints is not implemented yet")