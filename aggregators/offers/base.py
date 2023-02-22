from django.db import transaction

from aggregators.models import CollectionOffer, Collection
from nft_loans.configs.logger import logger


class OfferHandler:
    marketplace: str
    PAGE_SIZE = 50

    def __init__(self, marketplace: str):
        self.marketplace = marketplace

    def get_collection_offers(self, collection: Collection):
        raise NotImplementedError

    def get_all_offers(self):
        collections = Collection.objects.all()
        offers = []
        for collection in collections:
            offers += self.get_collection_offers(collection)
        return offers

    def handle(self):
        offers = self.get_all_offers()
        if len(offers) == 0:
            logger.error(f"[OfferHandler] {self.marketplace} no offers!")
            return

        with transaction.atomic():
            CollectionOffer.objects.filter(marketplace=self.marketplace).delete()
            CollectionOffer.objects.bulk_create(offers, 500, True)
            logger.info(f"[OfferHandler] {self.marketplace} Atomic offer is handled!")
