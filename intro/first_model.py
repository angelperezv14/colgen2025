def first_model():
    from pyscipopt import Model

    model = Model()

    # maximize x + y
    # subject to
    #  x + y <= 1
    #  x, y binary

    # TODO: 1. Create variables x and y
    x = model.addVar(vtype="B", name="x")
    y = model.addVar(vtype="B", name="y")

    # TODO: 2. Add the constraint x + y <= 1
    constraint = model.addCons(x + y <= 1, name="constraint")

    # TODO: 3. Set the objective function to maximize x + y
    model.setObjective(x + y, sense="maximize")
    return model
