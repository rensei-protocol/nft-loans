import requests

from aggregators.models import Collection, CollectionOffer
from aggregators.models.helper import ARCADE
from aggregators.offers.base import OfferHandler
from nft_loans.configs.logger import logger


class ArcadeOfferHandler(OfferHandler):
    def __init__(self):
        self.ARCADE_URL = (
            "https://api-v2.arcade.xyz/api/v2/loanterms?kind=collection&count=10000"
        )
        super().__init__(ARCADE)

    def serialize_order(self, data: dict, collection: Collection):
        offer = CollectionOffer(
            id=f"{ARCADE}_{data['id']}",  # pk
            marketplace=ARCADE,
            # base fields
            apr=-1,  # need to recalculate
            amount=float(data["principal"]),
            repayment=-1,
            expire_time=data["expiresAt"],
            duration=data["durationSecs"],
            erc20_address=data["payableCurrency"],
            lender=data["creatorId"],
            collection=collection,
            create_time=data["createdAt"],
            nonce=None,
            signature=None,
            # nftfi fields
            # arcade_metadata=data,
        )
        offer.apr = offer.calculate_apr_arcade_by_set_repayment(data["interestRate"])
        offer.set_essentials()
        return offer

    def get_collection_offers_without_query(
        self, collection: Collection, raw_orders: list
    ):
        logger.info(f"Processing {collection.address} - {collection.name}")
        orders = []
        for raw_order in raw_orders:
            if collection.address.lower() != raw_order["collectionId"].lower():
                continue
            orders.append(self.serialize_order(raw_order, collection))

        return orders

    def get_all_offers(self):
        """
        For arcade we need request api once, because there is no api by collection
        """
        collections = Collection.objects.all()
        offers = []

        try:
            raw_orders = requests.get(self.ARCADE_URL).json()
        except Exception as e:
            logger.error(e)
            return

        for collection in collections:
            offers += self.get_collection_offers_without_query(collection, raw_orders)
        return offers


# handler = ArcadeOfferHandler()
# handler.handle()
