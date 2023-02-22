import requests

# from django.utils.datetime_safe import datetime
from django.utils.timezone import datetime

from aggregators.fetchers.base import BaseFetcher
from aggregators.models import (
    ArcadeLoan,
    ArcadeLoanRepaid,
    ArcadeLoanRolledOver,
    ArcadeLoanClaimed,
)


class ArcadeFetcher(BaseFetcher):
    SUBGRAPH_URL = "https://api.studio.thegraph.com/query/42281/subgraph-arcade/v0.1.1"

    def get_repays(self, counter):
        query = f"""
        query ($skipAmount: Int) {{
            loanRepaids (
                 {self.get_common_conditions(model=ArcadeLoanRepaid)}
                 skip: $skipAmount
            ) {{
                loanId
                blockNumber
                blockTimestamp
                transactionHash
            }}
        }}
        """

        variables = {"skipAmount": counter}
        result = requests.post(
            url=self.SUBGRAPH_URL,
            json={"query": query, "variables": variables},
            timeout=5,
        )

        res = result.json()["data"]["loanRepaids"]
        return [
            ArcadeLoanRepaid(
                loan_id=int(x["loanId"]),
                block_time_stamp=datetime.utcfromtimestamp(float(x["blockTimestamp"])),
                block_number=x["blockNumber"],
                transaction_hash=x["transactionHash"],
            )
            for x in res
        ]

    def get_rolled_over(self, counter):
        query = f"""
        query ($skipAmount: Int) {{
            loanRolledOvers (
                 {self.get_common_conditions(model=ArcadeLoanRolledOver)}
                 skip: $skipAmount
            ) {{
                oldLoanId
                newLoanId
                blockNumber
                blockTimestamp
                transactionHash
            }}
        }}
        """

        variables = {"skipAmount": counter}
        result = requests.post(
            url=self.SUBGRAPH_URL,
            json={"query": query, "variables": variables},
            timeout=5,
        )

        res = result.json()["data"]["loanRolledOvers"]
        return [
            ArcadeLoanRolledOver(
                old_loan_id=int(x["oldLoanId"]),
                new_loan_id=int(x["newLoanId"]),
                block_time_stamp=datetime.utcfromtimestamp(float(x["blockTimestamp"])),
                block_number=x["blockNumber"],
                transaction_hash=x["transactionHash"],
            )
            for x in res
        ]

    def get_loan_claimed(self, counter):
        query = f"""
        query ($skipAmount: Int) {{
            loanClaimeds (
                 {self.get_common_conditions(model=ArcadeLoanClaimed)}
                 skip: $skipAmount
            ) {{
                loanId
                blockNumber
                blockTimestamp
                transactionHash
            }}
        }}
        """

        variables = {"skipAmount": counter}
        result = requests.post(
            url=self.SUBGRAPH_URL,
            json={"query": query, "variables": variables},
            timeout=5,
        )

        res = result.json()["data"]["loanClaimeds"]
        return [
            ArcadeLoanClaimed(
                loan_id=int(x["loanId"]),
                block_time_stamp=datetime.utcfromtimestamp(float(x["blockTimestamp"])),
                block_number=x["blockNumber"],
                transaction_hash=x["transactionHash"],
            )
            for x in res
        ]

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
	            transactionHash
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
                txhash=x["transactionHash"],
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

    def process_repays(self):
        raw_repays = self.get_all(self.get_repays)
        ArcadeLoanRepaid.objects.bulk_create(
            raw_repays,
            batch_size=self.BATCH_SIZE,
            ignore_conflicts=self.IGNORE_CONFLICTS,
        )

    def process_rolled_over(self):
        rolled_overs = self.get_all(self.get_rolled_over)
        ArcadeLoanRolledOver.objects.bulk_create(
            rolled_overs,
            batch_size=self.BATCH_SIZE,
            ignore_conflicts=self.IGNORE_CONFLICTS,
        )

    def process_claimeds(self):
        claimeds = self.get_all(self.get_loan_claimed)
        ArcadeLoanClaimed.objects.bulk_create(
            claimeds,
            batch_size=self.BATCH_SIZE,
            ignore_conflicts=self.IGNORE_CONFLICTS,
        )

    def handle(self):
        self.process_loans()
        self.process_repays()
        self.process_rolled_over()
        self.process_claimeds()
