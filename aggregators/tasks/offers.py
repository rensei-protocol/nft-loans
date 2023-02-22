from celery import group

from aggregators.models.helper import NFTFI, X2Y2, ARCADE
from aggregators.offers.arcade.main import ArcadeOfferHandler
from aggregators.offers.nftfi.main import NftfiOfferHandler
from aggregators.offers.x2y2.main import X2Y2OfferHandler
from nft_loans.celery import app
from nft_loans.configs.logger import logger

OFFER_CLASS_MAP = {
    NFTFI: NftfiOfferHandler,
    X2Y2: X2Y2OfferHandler,
    ARCADE: ArcadeOfferHandler,
}


@app.task
def call_offer(marketplace):
    try:
        handler_class = OFFER_CLASS_MAP[marketplace]
        offer_handler = handler_class()
        offer_handler.handle()
        return True
    except Exception as e:
        logger.error(e)
        return False


@app.task(name="update_offers")
def update_offers():
    MARKETPLACES_LIST = OFFER_CLASS_MAP.keys()
    # call child tasks in parallel using group
    tasks = group([call_offer.s(m) for m in MARKETPLACES_LIST])()
    tasks.forget()
