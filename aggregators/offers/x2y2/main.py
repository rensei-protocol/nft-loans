import os
import requests

from aggregators.models import X2Y2Offer


class X2Y2OffchainFetcher():
    model = X2Y2Offer
    BASE_URL = "https://loan-api.x2y2.org/v1/offer/list"
    collections = ["0xED5AF388653567Af2F388E6224dC7C4b3241C544"]
    API_KEY = os.getenv("X2Y2_API_KEY")

    def get_offers(self):
        headers = {'X-API-KEY': self.API_KEY, 'accept': 'application/json'}
        offers = []
        for addr in self.collections:
            more_page = True
            page = 1
            while more_page:
                params = {'nftAddress': addr, 'tokenId': '1', 'pageSize': '20', 'page': page}
                result = requests.get(self.BASE_URL, headers=headers, params=params)
                data = result.json()['data']
                more_page = data['more_page']
                page += 1
                items = data['list']
                offers.append([X2Y2Offer(
                    offer_id=x["offerId"],
                    token_id=x["tokenId"],
                    nft_address=x["nftAddress"],
                    amount=x["amount"],
                    repayment=x["repayment"],
                    apr=x["apr"],
                    lender=x["lender"],
                    expire_time=x["expireTime"],
                    extra=x["extra"],
                    duration=x["duration"],
                    erc20_address=x["erc20Address"],
                    nonce=x["nonce"],
                    signature=x["signature"],
                    status=x["status"],
                    create_time=x["createTime"]
                ) for x in items])
        return offers

    def handle(self):
        self.get_offers()
