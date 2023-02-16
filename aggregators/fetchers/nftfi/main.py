import requests
from django.utils.timezone import datetime

from aggregators.fetchers.base import BaseFetcher
from aggregators.models import (
    NftfiLoan,
    NftfiLiquidated,
    NftfiRepaid,
    NftfiRenegotiated,
)


class NftfiFetcher(BaseFetcher):
    model = NftfiLoan
    SUBGRAPH_URL = "https://api.studio.thegraph.com/query/42281/nftfi/v0.0.3"

    def get_loans(self, counter):
        """Gets loans up to 1000 results"""
        query = f"""
		    query ($skipAmount: Int) {{
		        loanStarteds(
	                {self.get_common_conditions(model=NftfiLoan)}
		            skip: $skipAmount
		        ) {{
		            id
		            loanId
		            borrower
		            lender
		            loanTerms_loanPrincipalAmount
		            loanTerms_maximumRepaymentAmount
		            loanTerms_nftCollateralId
		            loanTerms_loanERC20Denomination
		            loanTerms_loanDuration
		            loanTerms_loanInterestRateForDurationInBasisPoints
		            loanTerms_loanAdminFeeInBasisPoints
		            loanTerms_nftCollateralWrapper
		            loanTerms_loanStartTime
		            loanTerms_nftCollateralContract
		            loanTerms_borrower
		            loanExtras_revenueSharePartner
		            loanExtras_revenueShareInBasisPoints
		            loanExtras_referralFeeInBasisPoints
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
        res = result.json()["data"]["loanStarteds"]
        return [
            NftfiLoan(
                loan_id=int(x["loanId"]),
                block_time=datetime.utcfromtimestamp(float(x["blockTimestamp"])),
                block_number=x["blockNumber"],
                borrower=x["borrower"],
                lender=x["lender"],
                loan_principal_amount=x["loanTerms_loanPrincipalAmount"],
                maximum_repayment_amount=x["loanTerms_maximumRepaymentAmount"],
                nft_collateral_id=x["loanTerms_nftCollateralId"],
                loan_erc20_denomination=x["loanTerms_loanERC20Denomination"],
                loan_duration=x["loanTerms_loanDuration"],
                loan_interest_rate_for_duration_in_basis_points=x[
                    "loanTerms_loanInterestRateForDurationInBasisPoints"
                ],
                loan_admin_fee_in_basic_points=x["loanTerms_loanAdminFeeInBasisPoints"],
                loan_start_time=datetime.utcfromtimestamp(
                    float(x["loanTerms_loanStartTime"])
                ),
                nft_collateral_contract=x["loanTerms_nftCollateralContract"],
                revenue_share_partner=x["loanExtras_revenueSharePartner"],
                revenue_share_in_basis_points=x["loanExtras_revenueShareInBasisPoints"],
                referral_fee_in_basis_points=x["loanExtras_referralFeeInBasisPoints"],
                transaction_hash=x["transactionHash"],
            )
            for x in res
        ]

    def get_liquidates(self, counter):
        """Gets loans up to 1000 results"""
        query = f"""
                query ($skipAmount: Int) {{
                    loanLiquidateds (
                        {self.get_common_conditions(model=NftfiLiquidated)}
                        skip: $skipAmount
                    ) {{
                    blockNumber
                    blockTimestamp
                    borrower
                    id
                    lender
                    loanId
                    loanLiquidationDate
                    loanMaturityDate
                    loanPrincipalAmount
                    nftCollateralContract
                    nftCollateralId
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
            NftfiLiquidated(
                block_number=x["blockNumber"],
                block_time=datetime.utcfromtimestamp(float(x["blockTimestamp"])),
                borrower=x["borrower"],
                lender=x["lender"],
                loan_id=x["loanId"],
                loan_liquidation_date=datetime.utcfromtimestamp(
                    float(x["loanLiquidationDate"])
                ),
                loan_maturity_date=datetime.utcfromtimestamp(
                    float(x["loanMaturityDate"])
                ),
                loan_principal_amount=x["loanPrincipalAmount"],
                nft_collateral_contract=x["nftCollateralContract"],
                nft_collateral_id=x["nftCollateralId"],
                transaction_hash=x["transactionHash"],
            )
            for x in res
        ]

    def get_repaids(self, counter):
        """Gets loans up to 1000 results"""
        query = f"""
                query ($skipAmount: Int) {{
                    loanRepaids (
                        {self.get_common_conditions(model=NftfiRepaid)}
                        skip: $skipAmount
                    ) {{
                        adminFee
                        amountPaidToLender
                        blockNumber
                        blockTimestamp
                        borrower
                        lender
                        id
                        loanERC20Denomination
                        loanId
                        loanPrincipalAmount
                        nftCollateralContract
                        nftCollateralId
                        revenueShare
                        revenueSharePartner
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
            NftfiRepaid(
                admin_fee=x["adminFee"],
                amount_paid_to_lender=x["amountPaidToLender"],
                block_number=x["blockNumber"],
                block_time=datetime.utcfromtimestamp(float(x["blockTimestamp"])),
                borrower=x["borrower"],
                lender=x["lender"],
                loan_erc20_denomination=x["loanERC20Denomination"],
                loan_id=x["loanId"],
                loan_principal_amount=x["loanPrincipalAmount"],
                nft_collateral_contract=x["nftCollateralContract"],
                nft_collateral_id=x["nftCollateralId"],
                revenue_share=x["revenueShare"],
                revenue_share_partner=x["revenueSharePartner"],
                transaction_hash=x["transactionHash"],
            )
            for x in res
        ]

    def get_renegotiated(self, counter):
        """Gets loans up to 1000 results"""
        query = f"""
                query ($skipAmount: Int) {{
                    loanRenegotiateds (
                        {self.get_common_conditions(model=NftfiRenegotiated)}
                        skip: $skipAmount
                    ) {{
                        blockNumber
                        blockTimestamp
                        borrower
                        id
                        lender
                        loanId
                        newLoanDuration
                        newMaximumRepaymentAmount
                        renegotiationAdminFee
                        renegotiationFee
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
        res = result.json()["data"]["loanRenegotiateds"]
        return [
            NftfiRenegotiated(
                block_number=x["blockNumber"],
                block_time=datetime.utcfromtimestamp(float(x["blockTimestamp"])),
                borrower=x["borrower"],
                lender=x["lender"],
                loan_id=x["loanId"],
                new_loan_duration=x["newLoanDuration"],
                new_maximum_repayment_amount=x["newMaximumRepaymentAmount"],
                renegotiation_admin_fee=x["renegotiationAdminFee"],
                renegotiation_fee=x["renegotiationFee"],
                transaction_hash=x["transactionHash"],
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
        NftfiLoan.objects.bulk_create(
            raw_loans,
            batch_size=self.BATCH_SIZE,
            ignore_conflicts=self.IGNORE_CONFLICTS,
        )

    def process_liquidates(self):
        raw_loans = self.get_all(self.get_liquidates)
        NftfiLiquidated.objects.bulk_create(
            raw_loans,
            batch_size=self.BATCH_SIZE,
            ignore_conflicts=self.IGNORE_CONFLICTS,
        )

    def process_repays(self):
        raw_loans = self.get_all(self.get_repaids)
        NftfiRepaid.objects.bulk_create(
            raw_loans,
            batch_size=self.BATCH_SIZE,
            ignore_conflicts=self.IGNORE_CONFLICTS,
        )

    def process_renegotiates(self):
        raw_loans = self.get_all(self.get_renegotiated)
        NftfiRenegotiated.objects.bulk_create(
            raw_loans,
            batch_size=self.BATCH_SIZE,
            ignore_conflicts=self.IGNORE_CONFLICTS,
        )

    def handle(self):
        self.process_loans()
        self.process_liquidates()
        self.process_repays()
        self.process_renegotiates()
