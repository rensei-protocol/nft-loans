import itertools
import json
import time
from collections import defaultdict

import math


def get_all_permutations(offers: list):
    # generate all possible binary permutations for the length of lst
    binary_perms = itertools.product([0, 1], repeat=len(offers))

    # iterate over binary_perms and get the indices of lst where the binary value is 1
    for binary_perm in binary_perms:
        indices = [i for i, x in enumerate(binary_perm) if x == 1]
        # use the indices to get the elements from lst
        yield [offers[i] for i in indices]


def main(threshold, target_amount):
    with open(
        "recommendation_data.json",
        "r",
    ) as f:
        offers = json.load(f)
        combinations = get_all_permutations(offers)
        best_amount_offer = {
            "amount": 0,
            "fee": 0,
            "combination": [],
            "amount_diff": math.inf,
        }
        best_fee_offer = {
            "amount": 0,
            "fee": math.inf,
            "combination": [],
            "weight": math.inf,
        }
        for combination in combinations:
            collection_count = defaultdict(int)
            amount = 0.0
            fee = 0.0
            is_breaked = False
            for offer in combination:
                collection = offer["collection"]
                collection_count[collection] += 1
                if collection_count[collection] > threshold.get(collection, 0):
                    is_breaked = True
                    break
                amount += offer["amount"]
                fee += offer["fee"]

            if is_breaked or len(combination) == 0:
                continue
            # find best amount offers
            amount_diff = abs(target_amount - amount)
            if best_amount_offer["amount_diff"] > amount_diff:
                best_amount_offer["amount_diff"] = amount_diff
                best_amount_offer["amount"] = amount
                best_amount_offer["combination"] = combination
                best_amount_offer["fee"] = fee
            # find best fee offers
            weight = 0.5 * amount_diff + 0.5 * fee
            if best_fee_offer["weight"] > weight:
                best_fee_offer["fee"] = fee
                best_fee_offer["amount"] = amount
                best_fee_offer["combination"] = combination
                best_fee_offer["weight"] = weight
        return {
            "best_amount_offer": best_amount_offer,
            "best_fee_offer": best_fee_offer,
        }


if __name__ == "__main__":
    threshold = {
        "0xed5af388653567af2f388e6224dc7c4b3241c544": 3,
        "0xbd3531da5cf5857e7cfaa92426877b022e612cf8": 2,
    }
    start_time = time.time()
    print(main(threshold, 4.2264e19))
    finish_time = time.time()
    print(f"Total time: {finish_time- start_time}")
