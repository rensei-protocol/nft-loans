import requests

# from django.utils.datetime_safe import datetime
from django.utils.timezone import datetime

from aggregators.fetchers.base import BaseFetcher
from aggregators.models import (
    X2Y2Loan,
    ArcadeLoan,
)


class ArcadeFetcher(BaseFetcher):
    model = X2Y2Loan
    SUBGRAPH_URL = "https://api.studio.thegraph.com/query/30834/nft/enroheohnenrh"

    def get_loans(self, counter):
        """Gets loans up to 1000 results"""
        query = f"""
	    query ($skipAmount: Int) {{
	        loans (
	            {self.get_common_conditions(model=ArcadeLoan)}
	            skip: $skipAmount
	        ) {{
	            balance
	            balancePaid
	            blockNumber
	            borrower
	            collateralAddress
	            collateralId
	            deadline
	            durationSecs
	            id
	            interestRate
	            lateFeesAccrued
	            lender
	            numInstallments
	            numInstallmentsPaid
	            payableCurrency
	            principal
	            startDate
	            state
	            timestamp
	            txhash
	        }}
	    }}
	    """

        variables = {"skipAmount": counter}
        result = requests.post(
            url=self.SUBGRAPH_URL,
            json={"query": query, "variables": variables},
            timeout=5,
        )

        res = result.json()["data"]["loans"]
        return [
            ArcadeLoan(
                loan_id=int(x["id"]),
                block_time=datetime.utcfromtimestamp(x["timestamp"]),
                block_number=x["blockNumber"],
                borrower=x["borrower"],
                lender=x["lender"],
                borrow_amount=x["principal"],
                borrow_asset=x["payableCurrency"],
                loan_duration=x["durationSecs"],
                loan_start=datetime.utcfromtimestamp(float(x["startDate"])),
                loan_end=datetime.utcfromtimestamp(float(x["deadline"])),
                loan_repay_amount=self.get_loan_repay_amount(
                    x["interestRate"], x["principal"]
                ),
                nft_asset=x["collateralAddress"],
                nft_token_id=x["collateralId"],
                txhash=x["txhash"],
                state=x["state"],
                num_installments=x["numInstallments"],
                num_installments_paid=x["numInstallmentsPaid"],
                balance=x["balance"],
                balance_paid=x["balancePaid"],
                late_fees_accrued=x["lateFeesAccrued"],
                interest_rate=x["interestRate"],
            )
            for x in res
        ]

    def get_loan_repay_amount(self, ir, principal):
        return float(ir) / 1000 * float(principal)

    def get_all(self, func):
        """Gets all results of a query"""
        all_res = []
        counter = 0
        end = False

        while not end:
            res = func(counter)
            all_res += res
            counter += 1000

            if res == []:
                end = True

        return all_res

    def process_loans(self):
        raw_loans = self.get_all(self.get_loans)
        ArcadeLoan.objects.bulk_create(
            raw_loans,
            batch_size=self.BATCH_SIZE,
            ignore_conflicts=self.IGNORE_CONFLICTS,
        )

    def handle(self):
        self.process_loans()
