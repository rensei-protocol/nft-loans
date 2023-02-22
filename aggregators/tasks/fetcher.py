from aggregators.fetchers.arcade.main import ArcadeFetcher
from aggregators.fetchers.benddao.main import BenddaoFetcher
from aggregators.fetchers.nftfi.main import NftfiFetcher
from aggregators.fetchers.x2y2.main import X2Y2Fetcher
from aggregators.offers.nftfi.main import NftfiOfferHandler
from aggregators.offers.x2y2.main import X2Y2OffchainFetcher
from nft_loans.celery import app
from nft_loans.configs.logger import logger


@app.task(name="x2y2_fetch_task")
def x2y2_fetch_task():
    try:
        fetcher = X2Y2Fetcher()
        fetcher.handle()
    except Exception as e:
        logger.error(e)


@app.task(name="x2y2_offchain_fetch_task")
def x2y2_offchain_fetch_task():
    try:
        fetcher = X2Y2OffchainFetcher()
        fetcher.handle()
    except Exception as e:
        logger.error(e)


@app.task(name="nftfi_fetch_task")
def nftfi_fetch_task():
    try:
        fetcher = NftfiFetcher()
        fetcher.handle()
    except Exception as e:
        logger.error(e)

    try:
        offer_handler = NftfiOfferHandler()
        offer_handler.handle()
    except Exception as e:
        logger.error(e)


@app.task(name="arcade_fetch_task")
def arcade_fetch_task():
    try:
        fetcher = ArcadeFetcher()
        fetcher.handle()
    except Exception as e:
        logger.error(e)


@app.task(name="benddao_fetch_task")
def benddao_fetch_task():
    try:
        fetcher = BenddaoFetcher()
        fetcher.handle()
    except Exception as e:
        logger.error(e)
