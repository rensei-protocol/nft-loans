from dataclasses import dataclass
import requests
import datetime

import database

NFTFI_SUBGRAPH_URL = "https://api.studio.thegraph.com/query/42281/nftfi/v0.0.3"


@dataclass
class Loan:
    """Loan Class"""
    loan_id: int
    block_time: datetime
    block_number: str
    borrower: str
    lender: str
    loan_principal_amount: str
    maximum_repayment_amount: str
    nft_collateral_id: str
    loan_erc20_denomination: str
    loan_duration: str
    loan_interest_rate_for_duration_in_basis_points: int
    loan_admin_fee_in_basic_points: int
    loan_start_time: datetime
    nft_collateral_contract: str
    revenue_share_partner: str
    revenue_share_in_basis_points: int
    referral_fee_in_basis_points: int
    transaction_hash: str

    def to_tuple(self):
        return tuple(self.__dict__.values())


def get_loans(counter):
    """Gets loans up to 1000 results"""
    query = """
    query ($skipAmount: Int) {
        loanStarteds(
            orderBy: blockNumber,
            orderDirection: desc,
            first: 1000,
            skip: $skipAmount
        ) {
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
        }
    }
    """
    variables = {'skipAmount': counter}
    result = requests.post(
        url=NFTFI_SUBGRAPH_URL,
        json={'query': query, 'variables': variables},
        timeout=5
    )
    res = result.json()['data']['loanStarteds']
    return [
        Loan(
            loan_id=int(x['loanId']),
            block_time=datetime.datetime.utcfromtimestamp(float(x['blockTimestamp'])),
            block_number=x['blockNumber'],
            borrower=x['borrower'],
            lender=x['lender'],
            loan_principal_amount=x['loanTerms_loanPrincipalAmount'],
            maximum_repayment_amount=x['loanTerms_maximumRepaymentAmount'],
            nft_collateral_id=x['loanTerms_nftCollateralId'],
            loan_erc20_denomination=x['loanTerms_loanERC20Denomination'],
            loan_duration=x['loanTerms_loanDuration'],
            loan_interest_rate_for_duration_in_basis_points=x['loanTerms_loanInterestRateForDurationInBasisPoints'],
            loan_admin_fee_in_basic_points=x['loanTerms_loanAdminFeeInBasisPoints'],
            loan_start_time=datetime.datetime.utcfromtimestamp(float(x['loanTerms_loanStartTime'])),
            nft_collateral_contract=x['loanTerms_nftCollateralContract'],
            revenue_share_partner=x['loanExtras_revenueSharePartner'],
            revenue_share_in_basis_points=x['loanExtras_revenueShareInBasisPoints'],
            referral_fee_in_basis_points=x['loanExtras_referralFeeInBasisPoints'],
            transaction_hash=x['transactionHash']
        ) for x in res]

def get_all(func):
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

def process_loans():
    loans = get_all(get_loans)
    loans_fmt = [x.to_tuple() for x in loans]
    database.insert_into_nftfi_loans(loans_fmt)


process_loans()
