from aggregators.fetchers.listing.snowgnosis_parser import ListingSnowgnosisParser
from nft_loans.celery import app


@app.task(name="fetch_snowgnosis_listing")
def fetch_snowgnosis_listing():
    parser = ListingSnowgnosisParser()
    parser.handle()
