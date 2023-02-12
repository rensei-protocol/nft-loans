from dataclasses import dataclass
import requests
import datetime
import database
from IPython import embed

SUBGRAPH_URL = "https://api.studio.thegraph.com/query/30834/nft/enroheohnenrh"

@dataclass
class Loan:
    """Loan Class"""
    loan_id: int
    block_time: datetime
    block_number: str
    borrower: str
    lender: str
    borrow_amount: str
    borrow_asset: str
    loan_duration: str
    loan_start: datetime
    loan_end: datetime
    loan_repay_amount: str
    nft_asset: str
    nft_token_id: str
    txhash: str
    state: str
    num_installments: int
    num_installments_paid: int
    balance: str
    balance_paid: str
    late_fees_accrued: str
    interest_rate: str
    
    def to_tuple(self): 
        return tuple(self.__dict__.values())

def get_loans(counter):
    """Gets loans up to 1000 results"""
    query = """
    query ($skipAmount: Int) { 
        loans (
            orderBy: blockNumber, 
            orderDirection: desc,
            first: 1000,
            skip: $skipAmount
        ) {
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
        }
    }
    """

    variables = {'skipAmount': counter }
    result = requests.post(
        url=SUBGRAPH_URL,
        json={'query': query, 'variables': variables },
        timeout=5
    )

    print(result.json())
    res = result.json()['data']['loans']  
    return [
        Loan(
            loan_id=int(x['id']),
            block_time=datetime.datetime.utcfromtimestamp(x['timestamp']),
            block_number=x['blockNumber'],
            borrower=x['borrower'],
            lender=x['lender'],
            borrow_amount=x['principal'],
            borrow_asset=x['payableCurrency'],
            loan_duration=x['durationSecs'],
            loan_start=datetime.datetime.utcfromtimestamp(float(x['startDate'])),
            loan_end=datetime.datetime.utcfromtimestamp(float(x['deadline'])),
            loan_repay_amount=get_loan_repay_amount(x['interestRate'], x['principal']),
            nft_asset=x['collateralAddress'],
            nft_token_id=x['collateralId'],
            txhash=x['txhash'],
            state=x['state'],
            num_installments=x['numInstallments'],
            num_installments_paid=x['numInstallmentsPaid'],
            balance=x['balance'],
            balance_paid=x['balancePaid'],
            late_fees_accrued=x['lateFeesAccrued'],
            interest_rate=x['interestRate']
        ) for x in res]

def get_loan_repay_amount(ir, principal):
    return float(ir) / 1000 * float(principal)

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
    database.insert_into_arcade_loans(loans_fmt)

process_loans()