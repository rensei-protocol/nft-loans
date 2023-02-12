from dataclasses import dataclass
import requests
import datetime
import database

X2Y2_SUBGRAPH_URL = "https://api.studio.thegraph.com/query/40533/x2y2-loans/v0.0.1"

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
    nft_is_collection: bool
    txhash: str
    nonce: str
    admin_share: str

    def to_tuple(self): 
        return tuple(self.__dict__.values())

@dataclass
class LoanRepaid:
    """Loan Repaid Class"""
    loan_id: int
    block_time: datetime
    block_number: str
    borrower: str
    lender: str
    borrow_amount: str
    borrow_asset: str
    loan_repay_amount: str
    nft_asset: str
    nft_token_id: str
    txhash: str
    fee: str

    def to_tuple(self): 
        return tuple(self.__dict__.values())

@dataclass
class LoanLiquidation:
    """Loan Liquidation Class"""
    loan_id: int
    block_time: datetime
    block_number: str
    borrower: str
    lender: str
    borrow_amount: str
    nft_asset: str
    nft_token_id: str
    loan_liquidation_time: datetime
    loan_maturity_time: datetime
    txhash: str

    def to_tuple(self): 
        return tuple(self.__dict__.values())

@dataclass
class NonceCancel:
    """Loan Nonce Cancel Class"""
    nonce: str
    block_time: datetime
    block_number: str
    lender: str
    txhash: str

    def to_tuple(self): 
        return tuple(self.__dict__.values())

def get_loans(counter):
    """Gets loans up to 1000 results"""
    query = """
    query ($skipAmount: Int) { 
        loanStarteds (
            orderBy: blockTimestamp, 
            orderDirection: desc,
            first: 1000,
            skip: $skipAmount
        ) {
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
        }
    }
    """

    variables = {'skipAmount': counter }
    result = requests.post(
        url=X2Y2_SUBGRAPH_URL,
        json={'query': query, 'variables': variables },
        timeout=5
    )

    res = result.json()['data']['loanStarteds']  
    return [Loan(block_time=datetime.datetime.utcfromtimestamp(float(x['blockTimestamp'])),
        block_number=x['blockNumber'],
        borrower=x['borrower'],
        lender=x['lender'],
        borrow_amount=x['loanDetail_borrowAmount'],
        borrow_asset=x['loanDetail_borrowAsset'],
        loan_duration=x['loanDetail_loanDuration'],
        loan_start=datetime.datetime.utcfromtimestamp(float(x['loanDetail_loanStart'])),
        loan_end=datetime.datetime.utcfromtimestamp((int(x['loanDetail_loanStart']) + int(x['loanDetail_loanDuration']))),
        loan_id=int(x['loanId']),
        loan_repay_amount=x['loanDetail_repayAmount'],
        nft_asset=x['loanDetail_nftAsset'],
        nft_token_id=x['loanDetail_nftTokenId'],
        nft_is_collection=x['loanDetail_isCollection'],
        txhash=x['transactionHash'],
        admin_share=x['loanDetail_adminShare'],
        nonce=x['nonce']) for x in res]

def get_repaids(counter):
    """Gets loans repaid up to 1000 results"""
    query = """
    query ($skipAmount: Int) { 
        loanRepaids (
            orderBy: blockTimestamp, 
            orderDirection: desc,
            first: 1000,
            skip: $skipAmount
        ) {
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
        }
    }
    """

    variables = {'skipAmount': counter }
    result = requests.post(
        url=X2Y2_SUBGRAPH_URL,
        json={'query': query, 'variables': variables },
        timeout=5
    )

    res = result.json()['data']['loanRepaids']  
    return [LoanRepaid(
        loan_id=x['loanId'],
        block_time=datetime.datetime.utcfromtimestamp(float(x['blockTimestamp'])),
        block_number=x['blockNumber'],
        borrower=x['borrower'],
        lender=x['lender'],
        borrow_amount=x['borrowAmount'],
        borrow_asset=x['borrowAsset'],
        loan_repay_amount=x['repayAmount'],
        nft_asset=x['nftAsset'],
        nft_token_id=x['nftTokenId'],
        txhash=x['transactionHash'],
        fee=x['adminFee']) for x in res]

def get_liquidations(counter):
    """Gets loan liquidations up to 1000 results"""
    query = """
    query ($skipAmount: Int) { 
        loanLiquidateds (
            orderBy: blockTimestamp, 
            orderDirection: desc,
            first: 1000,
            skip: $skipAmount
        ) {
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
        }
    }
    """

    variables = {'skipAmount': counter }
    result = requests.post(
        url=X2Y2_SUBGRAPH_URL,
        json={'query': query, 'variables': variables },
        timeout=5
    )

    res = result.json()['data']['loanLiquidateds']  
    return [LoanLiquidation(
        loan_id=x['loanId'],
        block_time=datetime.datetime.utcfromtimestamp(float(x['blockTimestamp'])),
        block_number=x['blockNumber'],
        borrower=x['borrower'],
        lender=x['lender'],
        borrow_amount=x['borrowAmount'],
        nft_asset=x['nftAsset'],
        nft_token_id=x['nftTokenId'],
        loan_liquidation_time=datetime.datetime.utcfromtimestamp(float(x['loanLiquidationDate'])),
        loan_maturity_time=datetime.datetime.utcfromtimestamp(float(x['loanMaturityDate'])),
        txhash=x['transactionHash']) for x in res]

def get_nonce_cancelleds(counter):
    """Gets nonce cancelled up to 1000 results"""
    query = """
    query ($skipAmount: Int) { 
        nonceCancelleds (
            orderBy: blockTimestamp, 
            orderDirection: desc,
            first: 1000,
            skip: $skipAmount
        ) {
            lender
            nonce
            blockNumber
            blockTimestamp
            transactionHash
        }
    }
    """

    variables = {'skipAmount': counter }
    result = requests.post(
        url=X2Y2_SUBGRAPH_URL,
        json={'query': query, 'variables': variables },
        timeout=5
    )

    res = result.json()['data']['nonceCancelleds']  
    return [NonceCancel(
        nonce=x['nonce'],
        block_time=datetime.datetime.utcfromtimestamp(float(x['blockTimestamp'])),
        block_number=x['blockNumber'],
        lender=x['lender'],
        txhash=x['transactionHash']) for x in res]

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
    database.insert_into_loans(loans_fmt)

def process_repaids():
    repaids = get_all(get_repaids)
    repaids_formatted = [x.to_tuple() for x in repaids]
    database.insert_into_repaids(repaids_formatted)

def process_liquidations():
    liquidations = get_all(get_liquidations)
    liqs_formatted = [x.to_tuple() for x in liquidations]
    database.insert_into_liquidations(liqs_formatted)

def process_cancels():
    cancels = get_all(get_nonce_cancelleds)
    cancels_fmt = [x.to_tuple() for x in cancels]
    database.insert_into_nonce_cancelled(cancels_fmt)
