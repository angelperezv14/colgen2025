from pyscipopt import quicksum


def linear_knapsack(capacity, weights, values):
    from pyscipopt import Model
    model = Model()
    
    # TODO Implement a linear knapsack, as described in exercise 1
    n = len(values)
    # Create variables: x_i ∈ [0,1]
    x = {}
    for i in range(n):
        x[i] = model.addVar(lb=0.0, ub=1.0, vtype="C", name=f"x_{i}")

    # Add capacity constraint: sum(w_i * x_i) <= C
    model.addCons(sum(weights[i] * x[i] for i in range(n)) <= capacity)

    # Set objective: maximize sum(v_i * x_i)
    model.setObjective(sum(values[i] * x[i] for i in range(n)), sense="maximize")
    return model

def binary_knapsack(capacity, weights, values):
    from pyscipopt import Model
    model = Model()

    # TODO Implement a 0-1 knapsack, as described in exercise 2
    n = len(values)
    # Create variables: x_i ∈ [0,1]
    x = {}
    for i in range(n):
        x[i] = model.addVar(lb=0.0, ub=1.0, vtype="B", name=f"x_{i}")

    # Add capacity constraint: sum(w_i * x_i) <= C
    model.addCons(sum(weights[i] * x[i] for i in range(n)) <= capacity)

    # Set objective: maximize sum(v_i * x_i)
    model.setObjective(sum(values[i] * x[i] for i in range(n)), sense="maximize")
    return model

def integer_knapsack(capacity, weights, values):
    from pyscipopt import Model
    model = Model()

    # TODO Implement an integer knapsack, as described in exercise 3
    n = len(values)
    # Create variables: x_i ∈ [0,1]
    x = {}
    for i in range(n):
        x[i] = model.addVar(lb=0.0, vtype="I", name=f"x_{i}")

    # Add capacity constraint: sum(w_i * x_i) <= C
    model.addCons(sum(weights[i] * x[i] for i in range(n)) <= capacity)

    # Set objective: maximize sum(v_i * x_i)
    model.setObjective(sum(values[i] * x[i] for i in range(n)), sense="maximize")

    return model

def limited_knapsack(capacity, weights, values, max_items):
    from pyscipopt import Model
    model = Model()

    # TODO Implement a knapsack limited to 4 items, as described in exercise 4
    n = len(values)
    # Create variables: x_i ∈ [0,1]
    x = {}
    for i in range(n):
        x[i] = model.addVar(lb=0.0, vtype="I", name=f"x_{i}")

    # Add capacity constraint: sum(w_i * x_i) <= C
    model.addCons(sum(weights[i] * x[i] for i in range(n)) <= capacity)
    
    # Max item limit constraint
    model.addCons(sum(x[i] for i in range(n)) <= max_items, name="item_limit")

    # Set objective: maximize sum(v_i * x_i)
    model.setObjective(sum(values[i] * x[i] for i in range(n)), sense="maximize")

    return model
