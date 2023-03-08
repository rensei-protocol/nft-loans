from ortools.algorithms import pywrapknapsack_solver
from ortools.sat.python import cp_model

from aggregators.serializers import OfferViewSerializer


class RecommendationKnapsackMultiBin:
    RATIO_OPTIONS = {"FEE_OPTIMIZED": 99, "AMOUNT_OPTIMIZED": 1, "BALANCED": 51}

    def __init__(self, offers, currency, amount, threshold):
        self.offers = list(offers)
        self.currency = currency
        self.amount = amount
        self.threshold = threshold
        self.solver = pywrapknapsack_solver.KnapsackSolver(
            pywrapknapsack_solver.KnapsackSolver.KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER,
            "KnapsackExample",
        )

    def get_offer_args(self, fee_ratio):
        fee = []
        amounts = []
        max_amount = max(off.amount for off in self.offers)
        weight_bias = []
        AMOUNT_NORMALIZER = pow(10, self.currency.decimals - 5)
        for offer in self.offers:
            # wight will store weight in ASC, for now it consists only 100% normalized amount
            weight_bias.append(offer.amount / max_amount * 100)
            # reverse fee
            fee.append(1 / offer.apr * 100)
            # make amount fit into integer
            amounts.append(int(offer.amount / AMOUNT_NORMALIZER))

        max_fee = max(fee)
        for i in range(len(fee)):
            # normalize fee, previously it was reversed only
            fee[i] = fee[i] / max_fee * 100
            weight_bias[i] = int(fee_ratio * fee[i] + (1 - fee_ratio) * weight_bias[i])

        weights = amounts
        weight_limit = int(self.amount / AMOUNT_NORMALIZER)
        return weight_bias, weights, weight_limit

    def calculate(self, fee_percent=10):
        values, weights, weight_limit = self.get_offer_args(fee_percent / 100)
        model = cp_model.CpModel()

        # Create a dictionary to group items by type
        collection_offers = {}
        collection_values = {}
        collection_weights = {}
        for offer_index in range(len(self.offers)):
            offer = self.offers[offer_index]
            value = values[offer_index]
            weight = weights[offer_index]
            if self.offers[offer_index].collection in collection_offers:
                collection_offers[offer.collection].append(offer)
                collection_values[offer.collection].append(value)
                collection_weights[offer.collection].append(weight)
            else:
                collection_offers[offer.collection] = [offer]
                collection_values[offer.collection] = [value]
                collection_weights[offer.collection] = [weight]

        # Create a binary variable for each item to represent whether it is selected or not
        x = {}
        bin_index = 0
        for collection in collection_offers:
            for i in range(len(collection_offers[collection])):
                x[i, bin_index] = model.NewBoolVar(f"x_{i}_{bin_index}")

            bin_index += 1

        # Add constraints for each type of item
        bin_index = 0
        weights_cond = []
        objective = []
        for collection, offers_of_collection in collection_offers.items():
            # Constraint to ensure that collection will not exceed threshold num
            model.Add(
                sum(x[i, bin_index] for i in range(len(offers_of_collection)))
                <= self.threshold[collection.address]
            )

            # create value objective to maximize it
            for i in range(len(offers_of_collection)):
                objective.append(
                    cp_model.LinearExpr.Term(
                        x[i, bin_index], collection_values[collection][i]
                    )
                )

            # create total weight to limit it with weight_limit in future
            weights_cond += [
                x[i, bin_index] * collection_weights[collection][i]
                for i in range(len(offers_of_collection))
            ]
            bin_index += 1

        # Add a constraint that ensures the sum of all weights does not exceed total_weight
        # The amount packed in each bin cannot exceed its capacity.
        model.Add(sum(weights_cond) <= weight_limit)
        model.Maximize(cp_model.LinearExpr.Sum(objective))

        # Solve the problem
        solver = cp_model.CpSolver()
        status = solver.Solve(model)
        total_w_res = 0
        total_v_res = 0
        selected_items = []
        if status == cp_model.OPTIMAL:
            # Print the solution
            bin_index = 0
            for type, items in collection_offers.items():
                for i in range(len(items)):
                    if solver.Value(x[i, bin_index]) == 1:
                        selected_items.append(items[i])
                        total_w_res += items[i].fee
                        total_v_res += items[i].amount
                bin_index += 1
            # print(f"Total weight: {total_w_res}")
            # print(f"Total value: {total_v_res}")
            # print(f"Selected items: {selected_items}")
        return selected_items, total_v_res, total_w_res

    def get_recommendations(self):
        results = {}
        for tag, fee_percent in self.RATIO_OPTIONS.items():
            offers, total_amount, total_fee = self.calculate(fee_percent)
            key = f"{total_amount}_{total_fee}"
            if key in results:
                results[key]["tag"].append(tag)
                continue
            results[key] = {
                "total_amount": total_amount,
                "total_fee": total_fee,
                "offers": OfferViewSerializer(offers, many=True).data,
                "tag": [tag],
            }
        return results.values()
