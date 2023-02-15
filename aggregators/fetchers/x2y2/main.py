import requests

# from django.utils.datetime_safe import datetime
from django.utils.timezone import datetime
from aggregators.fetchers.base import BaseFetcher
from aggregators.models import X2Y2Loan, X2Y2NonceCancelled, X2Y2Repaid, X2Y2Liquidation


class X2Y2Fetcher(BaseFetcher):
    model = X2Y2Loan
    SUBGRAPH_URL = "https://api.studio.thegraph.com/query/40533/x2y2-loans/v0.0.1"

    def get_loans(self, counter):
        """Gets loans up to 1000 results"""
        query = f"""
		    query ($skipAmount: Int) {{
		        loanStarteds (
	                {self.get_common_conditions(model=X2Y2Loan)}
		            skip: $skipAmount
		        ) {{
		            blockTimestamp
		            blockNumber
		            borrower
		            id
		            lender
		            loanDetail_borrowAmount
		            loanDetail_adminShare
		            loanDetail_borrower
		            loanDetail_borrowAsset
		            loanDetail_loanDuration
		            loanDetail_isCollection
		            loanDetail_loanStart
		            loanDetail_nftAsset
		            loanDetail_nftTokenId
		            loanDetail_repayAmount
		            loanId
		            transactionHash
		            nonce
		        }}
		    }}
		    """

        variables = {"skipAmount": counter}
        result = requests.post(
            url=self.SUBGRAPH_URL,
            json={"query": query, "variables": variables},
            timeout=5,
        )

        res = result.json()["data"]["loanStarteds"]
        return [
            X2Y2Loan(
                block_time=datetime.utcfromtimestamp(float(x["blockTimestamp"])),
                block_number=x["blockNumber"],
                borrower=x["borrower"],
                lender=x["lender"],
                borrow_amount=x["loanDetail_borrowAmount"],
                borrow_asset=x["loanDetail_borrowAsset"],
                loan_duration=x["loanDetail_loanDuration"],
                loan_start=datetime.utcfromtimestamp(float(x["loanDetail_loanStart"])),
                loan_end=datetime.utcfromtimestamp(
                    (int(x["loanDetail_loanStart"]) + int(x["loanDetail_loanDuration"]))
                ),
                loan_id=int(x["loanId"]),
                loan_repay_amount=x["loanDetail_repayAmount"],
                nft_asset=x["loanDetail_nftAsset"],
                nft_token_id=x["loanDetail_nftTokenId"],
                nft_is_collection=x["loanDetail_isCollection"],
                txhash=x["transactionHash"],
                fee=x["loanDetail_adminShare"],
                nonce=x["nonce"],
            )
            for x in res
        ]

    def get_repaids(self, counter):
        """Gets loans repaid up to 1000 results"""
        query = f"""
	    query ($skipAmount: Int) {{
	        loanRepaids (
	            {self.get_common_conditions(model=X2Y2Repaid)}
	            skip: $skipAmount
	        ) {{
	            loanId
	            blockTimestamp
	            blockNumber
	            borrower
	            lender
	            borrowAmount
	            borrowAsset
	            repayAmount
	            nftAsset
	            nftTokenId
	            transactionHash
	            adminFee
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
            X2Y2Repaid(
                loan_id=x["loanId"],
                block_time=datetime.utcfromtimestamp(float(x["blockTimestamp"])),
                block_number=x["blockNumber"],
                borrower=x["borrower"],
                lender=x["lender"],
                borrow_amount=x["borrowAmount"],
                borrow_asset=x["borrowAsset"],
                loan_repay_amount=x["repayAmount"],
                nft_asset=x["nftAsset"],
                nft_token_id=x["nftTokenId"],
                txhash=x["transactionHash"],
                fee=x["adminFee"],
            )
            for x in res
        ]

    def get_liquidations(self, counter):
        """Gets loan liquidations up to 1000 results"""
        query = f"""
	    query ($skipAmount: Int) {{
	        loanLiquidateds (
	            {self.get_common_conditions(model=X2Y2Liquidation)}
	            skip: $skipAmount
	        ) {{
	            loanId
	            blockTimestamp
	            blockNumber
	            borrower
	            lender
	            borrowAmount
	            nftAsset
	            nftTokenId
	            loanLiquidationDate
	            loanMaturityDate
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

        res = result.json()["data"]["loanLiquidateds"]
        return [
            X2Y2Liquidation(
                loan_id=x["loanId"],
                block_time=datetime.utcfromtimestamp(float(x["blockTimestamp"])),
                block_number=x["blockNumber"],
                borrower=x["borrower"],
                lender=x["lender"],
                borrow_amount=x["borrowAmount"],
                nft_asset=x["nftAsset"],
                nft_token_id=x["nftTokenId"],
                loan_liquidation_time=datetime.utcfromtimestamp(
                    float(x["loanLiquidationDate"])
                ),
                loan_maturity_time=datetime.utcfromtimestamp(
                    float(x["loanMaturityDate"])
                ),
                txhash=x["transactionHash"],
            )
            for x in res
        ]

    def get_nonce_cancelleds(self, counter):
        """Gets nonce cancelled up to 1000 results"""
        query = f"""
	    query ($skipAmount: Int) {{
	        nonceCancelleds (
	            {self.get_common_conditions(model=X2Y2NonceCancelled)}
	            skip: $skipAmount
	        ) {{
	            lender
	            nonce
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

        res = result.json()["data"]["nonceCancelleds"]
        return [
            X2Y2NonceCancelled(
                nonce=x["nonce"],
                block_time=datetime.utcfromtimestamp(float(x["blockTimestamp"])),
                block_number=x["blockNumber"],
                lender=x["lender"],
                txhash=x["transactionHash"],
            )
            for x in res
        ]

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
        X2Y2Loan.objects.bulk_create(
            raw_loans,
            batch_size=self.BATCH_SIZE,
            ignore_conflicts=self.IGNORE_CONFLICTS,
        )

    def process_repaids(self):
        raw_repaids = self.get_all(self.get_repaids)
        X2Y2Repaid.objects.bulk_create(
            raw_repaids,
            batch_size=self.BATCH_SIZE,
            ignore_conflicts=self.IGNORE_CONFLICTS,
        )

    def process_liquidations(self):
        raw_liquidations = self.get_all(self.get_liquidations)
        X2Y2Liquidation.objects.bulk_create(
            raw_liquidations,
            batch_size=self.BATCH_SIZE,
            ignore_conflicts=self.IGNORE_CONFLICTS,
        )

    def process_cancels(self):
        raw_cancels = self.get_all(self.get_nonce_cancelleds)
        X2Y2NonceCancelled.objects.bulk_create(
            raw_cancels,
            batch_size=self.BATCH_SIZE,
            ignore_conflicts=self.IGNORE_CONFLICTS,
        )

    def handle(self):
        self.process_loans()
        self.process_repaids()
        self.process_liquidations()
        self.process_cancels()
