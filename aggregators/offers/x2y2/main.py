import os
from datetime import datetime

import requests

from aggregators.models import Collection, CollectionOffer
from aggregators.models.helper import X2Y2
from aggregators.offers.base import OfferHandler


class X2Y2OfferHandler(OfferHandler):
    model = CollectionOffer
    BASE_URL = "https://loan-api.x2y2.org/v1/offer/list"
    API_KEY = os.getenv("X2Y2_API_KEY")

    def __init__(self):
        super().__init__(X2Y2)

    def get_collection_offers(self, collection: Collection):
        headers = {"X-API-KEY": self.API_KEY, "accept": "application/json"}
        offers = []
        addr = collection.address
        more_page = True
        page = 1
        while more_page:
            params = {
                "nftAddress": addr,
                "tokenId": "1",
                "pageSize": self.PAGE_SIZE,
                "page": page,
            }
            result = requests.get(
                self.BASE_URL,
                headers=headers,
                params=params,
                timeout=5,
            )
            data = result.json()["data"]
            more_page = data["more_page"]
            page += 1
            items = data["list"]
            for x in items:
                offer = CollectionOffer(
                    id=f"{X2Y2}_{x['offerId']}",  # pk
                    marketplace=X2Y2,
                    # base class fields
                    apr=round(float(x["apr"]) / 100, 1),
                    amount=float(x["amount"]),
                    repayment=float(x["repayment"]),
                    expire_time=datetime.utcfromtimestamp(float(x["expireTime"])),
                    duration=x["duration"],
                    erc20_address=x["erc20Address"],
                    lender=x["lender"],
                    collection=collection,
                    create_time=datetime.utcfromtimestamp(float(x["createTime"])),
                    nonce=x["nonce"],
                    signature=x["signature"],
                    # x2y2 fields
                    x2y2_metadata=x,
                )
                offer.set_essentials()
                offers.append(offer)
        return offers
