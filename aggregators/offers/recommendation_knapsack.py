import json

from ortools.algorithms import pywrapknapsack_solver

threshold = {
    "0xed5af388653567af2f388e6224dc7c4b3241c544": 3,
    "0xbd3531da5cf5857e7cfaa92426877b022e612cf8": 3,
}

import matplotlib.pyplot as plt

DECIMAL = 18


def plot():
    with open(
        "recommendation_data.json",
        "r",
    ) as f:
        offers = json.load(f)
        fee = []
        amounts = []
        apr = []
        max_amount = max(off["amount"] for off in offers)
        for offer in offers:
            fee.append(1 / offer["apr"] * 100)
            amounts.append(offer["amount"] / max_amount * 100)
            apr.append(offer["apr"])
        weight = []
        max_fee = max(fee)
        for i in range(len(fee)):
            fee[i] = fee[i] / max_fee * 100
            weight.append(0.5 * fee[i] + 0.5 * amounts[i])
        # plt.rcParams["figure.figsize"] = [7.00, 3.50]
        plt.rcParams["figure.autolayout"] = True
        fig, ax1 = plt.subplots()
        fee.sort()
        ax1.plot(fee, color="red")

        ax2 = ax1.twinx()
        amounts.sort()
        ax2.plot(amounts, color="blue")

        ax3 = ax1.twinx()
        weight.sort()
        ax3.plot(weight, color="y")
        fig.tight_layout()
        plt.show()


def get_offer_args(fee_ratio=0.1):
    with open(
        "recommendation_data.json",
        "r",
    ) as f:
        offers = json.load(f)
        fee = []
        amounts = []
        threshold_weight = []
        max_amount = max(off["amount"] for off in offers)
        weight_bias = []
        AMOUNT_NORMALIZER = pow(10, DECIMAL - 5)
        for offer in offers:
            # wight will store weight in ASC, for now it consists only 100% normalized amount
            weight_bias.append(offer["amount"] / max_amount * 100)
            # reverse fee
            fee.append(1 / offer["apr"] * 100)
            # make amount fit into integer
            amounts.append(offer["amount"] / AMOUNT_NORMALIZER)
            # collection threshold condition
            collection = offer["collection"]
            threshold_weight.append(1 if collection in threshold else 1000000)

        max_fee = max(fee)
        for i in range(len(fee)):
            # normalize fee, previously it was reversed only
            fee[i] = fee[i] / max_fee * 100
            weight_bias[i] = fee_ratio * fee[i] + (1 - fee_ratio) * weight_bias[i]

        weights = [amounts, threshold_weight]
        capacities = [4.2264e19 / AMOUNT_NORMALIZER, sum(threshold.values())]
        return weight_bias, weights, capacities


def check_result(packed_items):
    with open(
        "recommendation_data.json",
        "r",
    ) as f:
        offers = json.load(f)
        amount = 0.0
        for item in packed_items:
            amount += offers[item]["amount"]
            print(f"Apr: {offers[item]['apr']}")
        print(f"Amount: {amount} <= {4.2264e19}, cond {amount <= 4.2264e19}")
        return amount


def main():
    # Create the solver.
    solver = pywrapknapsack_solver.KnapsackSolver(
        pywrapknapsack_solver.KnapsackSolver.KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER,
        "KnapsackExample",
    )

    y = []
    x = []

    for percent in range(0, 100, 10):
        values, weights, capacities = get_offer_args(percent / 100)
        print(values, weights, capacities)

        solver.Init(values, weights, capacities)
        computed_value = solver.Solve()

        packed_items = []
        packed_weights = []
        total_weight = 0
        print("Total value =", computed_value)
        for i in range(len(values)):
            if solver.BestSolutionContains(i):
                packed_items.append(i)
                packed_weights.append(weights[0][i])
                total_weight += weights[0][i]
        print("Total weight:", total_weight)
        print("Packed items:", packed_items)
        print("Packed_weights:", packed_weights)

        amount = check_result(packed_items)

        x.append(percent)
        y.append(amount)

    plt.plot(x, y)
    plt.axhline(y=4.2264e19)
    plt.show()


if __name__ == "__main__":
    main()
    plot()
