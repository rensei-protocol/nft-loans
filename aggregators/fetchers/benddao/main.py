import requests
from django.utils.timezone import datetime
from aggregators.fetchers.base import BaseFetcher
from aggregators.models import BenddaoLiquidate, BenddaoBorrow, BenddaoRedeem
from nft_loans.configs.logger import logger


class BenddaoFetcher(BaseFetcher):
	SUBGRAPH_URL = "https://api.thegraph.com/subgraphs/name/readmost/benddao-mainnet"

	def get_liquidations(self, counter):
		"""Gets loans up to 1000 results"""
		query = """
	    query ($skipAmount: Int) { 
	        liquidates (
	            orderBy: blockNumber, 
	            orderDirection: desc,
	            first: 1000,
	            skip: $skipAmount
	        ) {
				borrower
				id
				nftAsset
				nftTokenId
				loanId
				blockTimestamp
				blockNumber
				user
				transactionHash    
				reserve    
				repayAmount
				remainAmount
	        }
	    }
	    """

		variables = {'skipAmount': counter }
		result = requests.post(
			url=self.SUBGRAPH_URL,
			json={'query': query, 'variables': variables },
			timeout=5
		)


		res = result.json()['data']['liquidates']
		return [
			BenddaoLiquidate(
				id=x['id'],
				block_number=int(x['blockNumber']),
				block_timestamp=datetime.utcfromtimestamp(float(x['blockTimestamp'])),
				borrower=x['borrower'],
				loan_id=int(x['loanId']),
				nft_asset=x['nftAsset'],
				nft_token_id=x['nftTokenId'],
				remain_amount=x['remainAmount'],
				repay_amount=x['repayAmount'],
				reserve=x['reserve'],
				transaction_hash=x['transactionHash'],
				user=x['user'],
			) for x in res]


	def get_borrows(self, counter):
		"""Gets loans up to 1000 results"""
		query = """
	    query ($skipAmount: Int) { 
	        borrows (
	            orderBy: blockNumber, 
	            orderDirection: desc,
	            first: 1000,
	            skip: $skipAmount
	        ) {
				amount
			    blockNumber
			    blockTimestamp
			    borrowRate
			    id
			    loanId
			    nftAsset
			    nftTokenId
			    onBehalfOf
			    referral
			    reserve
			    transactionHash
			    user
	        }
	    }
	    """

		variables = {'skipAmount': counter }
		result = requests.post(
			url=self.SUBGRAPH_URL,
			json={'query': query, 'variables': variables },
			timeout=5
		)

		try:
			res = result.json()['data']['borrows']
		except Exception as e:
			logger.error(e)
			return []

		return [
			BenddaoBorrow(
				id=x['id'],
				block_number=int(x['blockNumber']),
				block_timestamp=datetime.utcfromtimestamp(float(x['blockTimestamp'])),
				loan_id=int(x['loanId']),
				user=x['user'],
				on_behalf_of=x['onBehalfOf'],
				nft_token_id=x['nftTokenId'],
				nft_asset=x['nftAsset'],
				transaction_hash=x['transactionHash'],
				reserve=x['reserve'],
				referral=int(x['referral']),
				borrow_rate=x['borrowRate'],
				amount=x['amount'],
			) for x in res]

	def get_redeems(self, counter):
		"""Gets loans up to 1000 results"""
		query = """
	    query ($skipAmount: Int) { 
	        redeems (
	            orderBy: blockNumber, 
	            orderDirection: desc,
	            first: 1000,
	            skip: $skipAmount
	        ) {
				    blockNumber
				    blockTimestamp
				    borrowAmount
				    borrower
				    fineAmount
				    id
				    loanId
				    nftAsset
				    nftTokenId
				    reserve
				    transactionHash
				    user
	        }
	    }
	    """

		variables = {'skipAmount': counter }
		result = requests.post(
			url=self.SUBGRAPH_URL,
			json={'query': query, 'variables': variables },
			timeout=5
		)


		res = result.json()['data']['redeems']
		return [
			BenddaoRedeem(
				id=x['id'],
				block_number=int(x['blockNumber']),
				block_timestamp=datetime.utcfromtimestamp(float(x['blockTimestamp'])),
				borrow_amount=x['borrowAmount'],
				borrower=x['borrower'],
				fine_amount=x['fineAmount'],
				loan_id=int(x['loanId']),
				nft_asset=x['nftAsset'],
				nft_token_id=x['nftTokenId'],
				reserve=x['reserve'],
				transaction_hash=x['transactionHash'],
				user=x['user'],
			) for x in res]

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

	def process_liquidations(self):
		raw_loans = self.get_all(self.get_liquidations)
		BenddaoLiquidate.objects.bulk_create(raw_loans, batch_size=self.BATCH_SIZE, ignore_conflicts=self.IGNORE_CONFLICTS)

	def process_borrows(self):
		raw_loans = self.get_all(self.get_borrows)
		BenddaoBorrow.objects.bulk_create(raw_loans, batch_size=self.BATCH_SIZE, ignore_conflicts=self.IGNORE_CONFLICTS)

	def process_redeems(self):
		raw_loans = self.get_all(self.get_redeems)
		BenddaoRedeem.objects.bulk_create(raw_loans, batch_size=self.BATCH_SIZE, ignore_conflicts=self.IGNORE_CONFLICTS)


	def handle(self):
		self.process_liquidations()
		self.process_borrows()
		self.process_redeems()