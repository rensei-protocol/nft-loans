from ortools.algorithms import pywrapknapsack_solver

from aggregators.serializers import OfferViewSerializer


class RecommendationKnapsack:
    RATIO_OPTIONS = {"FEE_OPTIMIZED": 100, "AMOUNT_OPTIMIZED": 0, "BALANCED": 60}

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
        threshold_weight = []
        max_amount = max(off.amount for off in self.offers)
        weight_bias = []
        AMOUNT_NORMALIZER = pow(10, self.currency.decimals - 5)
        for offer in self.offers:
            # wight will store weight in ASC, for now it consists only 100% normalized amount
            weight_bias.append(offer.amount / max_amount * 100)
            # reverse fee
            fee.append(1 / offer.apr * 100)
            # make amount fit into integer
            amounts.append(offer.amount / AMOUNT_NORMALIZER)
            # collection threshold condition
            collection = offer.collection.address.lower()
            threshold_weight.append(1 if collection in self.threshold else 1000000)

        max_fee = max(fee)
        for i in range(len(fee)):
            # normalize fee, previously it was reversed only
            fee[i] = fee[i] / max_fee * 100
            weight_bias[i] = fee_ratio * fee[i] + (1 - fee_ratio) * weight_bias[i]

        weights = [amounts, threshold_weight]
        capacities = [self.amount / AMOUNT_NORMALIZER, sum(self.threshold.values())]
        return weight_bias, weights, capacities

    def calculate(self, fee_percent=10):
        values, weights, capacities = self.get_offer_args(fee_percent / 100)
        self.solver.Init(values, weights, capacities)
        self.solver.Solve()

        packed_items = []
        total_amount = 0.0
        total_fee = 0.0
        for i in range(len(values)):
            if self.solver.BestSolutionContains(i):
                packed_items.append(i)
                total_amount += self.offers[i].amount
                total_fee += self.offers[i].fee
        return list(map(self.offers.__getitem__, packed_items)), total_amount, total_fee

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
