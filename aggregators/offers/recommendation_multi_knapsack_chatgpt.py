from ortools.sat.python import cp_model


class Item:
    def __init__(self, value, weight, type):
        self.value = value
        self.weight = weight
        self.type = type

    def __repr__(self):
        return f"({self.type} v:{self.value} w:{self.weight})"


def solve_knapsack(items, total_weight, thresholds):
    model = cp_model.CpModel()

    # Create a dictionary to group items by type
    type_items = {}
    for item in items:
        if item.type in type_items:
            type_items[item.type].append(item)
        else:
            type_items[item.type] = [item]

    # Create a binary variable for each item to represent whether it is selected or not
    x = {}
    bin_index = 0
    for b in type_items:
        for i in range(len(type_items[b])):
            x[i, bin_index] = model.NewBoolVar(f"x_{i}_{bin_index}")
            # x[i, bin_index] = model.NewIntVar(
            #     model, int(b == type_items[b][i].type), f"x_{i}_{bin_index}"
            # )
        bin_index += 1

    # Add constraints for each type of item
    # knapsacks = [None] * len(type_items)
    bin_index = 0
    weights = []
    objective = []
    for type, items in type_items.items():
        # knapsacks[bin_index] = model.NewIntVar(0, total_weight, f"knapsack_{bin_index}")

        # Add a constraint that limits the number of items of this type that can be selected
        objective_w = []
        for i in range(len(items)):
            objective_w.append(
                cp_model.LinearExpr.Term(x[i, bin_index], items[i].weight)
            )
        model.Maximize(cp_model.LinearExpr.Sum(objective_w))

        model.Add(
            sum(x[i, bin_index] for i in range(len(items)))
            <= thresholds.get(type, len(items))
        )

        # Add a constraint that ensures that all items of the same type are in the same knapsack
        # model.Add(sum(x[item] for item in items) <= 1)
        # model.Add(
        #     sum(x[i, bin_index] * items[i].weight for i in range(len(items)))
        #     <= knapsacks[bin_index]
        # )

        # Add weight and value constraints for the items of this type

        for i in range(len(items)):
            objective.append(cp_model.LinearExpr.Term(x[i, bin_index], items[i].value))

        weights += [x[i, bin_index] * items[i].weight for i in range(len(items))]
        bin_index += 1

    # Add a constraint that ensures the sum of all weights does not exceed total_weight
    # The amount packed in each bin cannot exceed its capacity.
    model.Add(sum(weights) <= total_weight)
    model.Maximize(cp_model.LinearExpr.Sum(objective))

    # Solve the problem
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    total_w_res = 0
    total_v_res = 0
    if status == cp_model.OPTIMAL:
        # Print the solution
        selected_items = []
        bin_index = 0
        for type, items in type_items.items():
            for i in range(len(items)):
                if solver.Value(x[i, bin_index]) == 1:
                    selected_items.append(items[i])
                    total_w_res += items[i].weight
                    total_v_res += items[i].value
            bin_index += 1
        print(f"Total weight: {total_w_res}")
        print(f"Total value: {total_v_res}")
        print(f"Selected items: {selected_items}")


# Example usage
items = [
    Item(value=1, weight=10, type="A"),
    Item(value=1, weight=20, type="A"),
    Item(value=1, weight=30, type="A"),
    Item(value=1, weight=40, type="A"),
    Item(value=2, weight=50, type="A"),
    Item(value=1, weight=10, type="B"),
    Item(value=1, weight=20, type="B"),
    Item(value=1, weight=10, type="C"),
    Item(value=1, weight=20, type="C"),
]
total_weight = 110
thresholds = {"A": 1, "B": 1, "C": 3}
solve_knapsack(items, total_weight, thresholds)
