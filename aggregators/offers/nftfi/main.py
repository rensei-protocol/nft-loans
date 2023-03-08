import os
from datetime import datetime

import requests

from aggregators.models import Collection, CollectionOffer
from aggregators.models.helper import NFTFI
from aggregators.offers.base import OfferHandler
from nft_loans.configs.logger import logger


class NftfiOfferHandler(OfferHandler):
    def __init__(self):
        self.auth_payload = {
            "message": 'Welcome to NFTfi!\r\nClick "Sign" to sign in. No password needed!\r\n\r\nThis message proves you own this wallet address : 0xEB8fb2f6D41706759B8544D5adA16FC710211ca2 \r\n\r\nBy signing this message you agree to our terms and conditions, available at: \r\nhttps://nftfi.com/terms-and-conditions/ \r\nhttps://nftfi.com/terms-of-use/ \r\nversion hash: 9717efa',
            "nonce": "101738587932585587244283248546180774891136035089181550845298539632806086033486",
            "signedMessage": "0xe66dea23c115041ce494cea73a613768f27c612fb4b2149cec087a3d0b70d62a1b1f92ab1e5b0c587c9637e24c1ee49ad0e27ea005d05400ff8c615e92c35b5a1c",
            "accountAddress": "0xEB8fb2f6D41706759B8544D5adA16FC710211ca2",
        }
        self.NFTFI_KEY = os.getenv("NFTFI_KEY")
        self.NFTFI_SDK_URL = os.getenv("NFTFI_SDK_URL")
        super().__init__(NFTFI)

    def get_bearer_token(self):
        url = self.NFTFI_SDK_URL + "/authorization/token"
        try:
            resp = requests.post(
                url,
                data=self.auth_payload,
                headers={"x-api-key": self.NFTFI_KEY},
            ).json()
            return resp["result"]["token"]
        except Exception as e:
            logger.error(e)
            return None

    def serialize_order(self, data: dict, collection: Collection):
        offer = CollectionOffer(
            id=f"{NFTFI}_{data['id']}",  # pk
            marketplace=NFTFI,
            # base fields
            apr=-1,  # need to recalculate
            amount=float(data["terms"]["loan"]["principal"]),
            repayment=float(data["terms"]["loan"]["repayment"]),
            expire_time=datetime.utcfromtimestamp(
                float(data["terms"]["loan"]["expiry"])
            ),
            duration=data["terms"]["loan"]["duration"],
            erc20_address=data["terms"]["loan"]["currency"],
            lender=data["lender"]["address"],
            collection=collection,
            create_time=data["date"]["offered"],
            nonce=data["lender"]["nonce"],
            signature=data["signature"],
            # nftfi fields
            # nftfi_metadata=data,
        )
        offer.apr = offer.calculate_apr()
        offer.set_essentials()
        return offer

    def get_collection_offers(self, collection: Collection):
        logger.info(f"Processing {collection.address} - {collection.name}")
        url = self.NFTFI_SDK_URL + "/offers"
        params = {
            "nftAddress": collection.address,
            "lenderAddressNe": "0xEB8fb2f6D41706759B8544D5adA16FC710211ca2",
            "contractName": "v2.loan.fixed.collection",
            "page": 1,
            "limit": self.PAGE_SIZE,
            "sort": "offerDate",
            "direction": "asc",
        }
        headers = {
            "Authorization": f"Bearer {self.get_bearer_token()}",
            "x-api-key": self.NFTFI_KEY,
        }
        orders = []
        current_page, total_pages = 1, 1
        is_first = True
        while current_page <= total_pages:
            try:
                raw_orders = requests.get(
                    url,
                    params=params,
                    headers=headers,
                ).json()
                for raw_order in raw_orders["results"]:
                    orders.append(self.serialize_order(raw_order, collection))

                if is_first:
                    is_first = False
                    total = int(raw_orders["pagination"]["total"])
                    total_pages = total // self.PAGE_SIZE
                    total_pages += 1 if total % self.PAGE_SIZE > 0 else 0

                logger.debug(
                    f"iter={current_page} is finished in nftfi orders querying!"
                )
            except Exception as e:
                logger.error(e)

            current_page += 1
            params["page"] = current_page
        return orders


# handler = NftfiOfferHandler()
# handler.save_all_offers()
