from typing import List
from pyscipopt import Model, quicksum

def binpacking_compact(sizes: List[int], capacity: int) -> Model:
    model = Model("Binpacking")
    
    # TODO: Implement the compact bin packing formulation
    n = len(sizes)
    # Upper bound: 1 bin per item
    bins = range(n)
    items = range(n)

    # Decision variables
    x = {(i, b): model.addVar(vtype="B", name=f"x_{i}_{b}") for i in items for b in bins}
    y = {b: model.addVar(vtype="B", name=f"y_{b}") for b in bins}

    # Constraint (2): each item assigned to one bin
    for i in items:
        model.addCons(sum(x[i, b] for b in bins) == 1, name=f"assign_{i}")

    # Constraint (3): capacity respected in each bin
    for b in bins:
        model.addCons(sum(sizes[i] * x[i, b] for i in items) <= capacity * y[b], name=f"capacity_{b}")

    # Objective: minimize number of bins used
    model.setObjective(sum(y[b] for b in bins), "minimize")

    return model