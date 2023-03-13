import base64
import json
from datetime import datetime

import requests

from aggregators.models import Collection, Listing
from aggregators.models.helper import SNOWGNESIS_LISTING_PROTOCOLS
from aggregators.serializers.listing import (
    DesiredTermsSerializer,
    TokenDataSerializer,
    BorrowerStatsSerializer,
)
from nft_loans.configs.logger import logger


class ListingSnowgnosisParser:
    URL = "https://nft.snowgenesis.com/api/v1/loan_listings"
    NESTED_QUERY_LIMIT = 4

    def __init__(self):
        self.supported_collections = set(Collection.get_all_collections())

    def decode_cursor(self, cursor_str):
        decoded_data = base64.urlsafe_b64decode(cursor_str + "==")
        # Convert the decoded data to a JSON object
        return json.loads(decoded_data)

    def serialize(self, listings_json):
        listings = []
        for listing_json in listings_json:
            desired_terms = DesiredTermsSerializer(
                data=listing_json["desiredTerms"], allow_null=True
            )
            borrower_stats = BorrowerStatsSerializer(
                data=listing_json["borrowerStats"], allow_null=True
            )
            token_data = TokenDataSerializer(
                data=listing_json["tokenData"], allow_null=True
            )
            desired_terms.is_valid()
            borrower_stats.is_valid()
            token_data.is_valid()

            marketplace = SNOWGNESIS_LISTING_PROTOCOLS.get(
                listing_json["protocol"], None
            )
            if not marketplace:
                continue

            collection = listing_json["collection"].lower()
            if not collection in self.supported_collections:
                continue

            listings.append(
                Listing(
                    marketplace=marketplace,
                    listing_id=listing_json["listingId"],
                    collection=Collection.objects.get(address=collection),
                    token_id=listing_json["tokenId"],
                    borrower=listing_json["borrower"],
                    listed_at=datetime.utcfromtimestamp(
                        float(listing_json["listedAt"])
                    ),
                    desired_terms=desired_terms.data,
                    borrower_stats=borrower_stats.data,
                    vaulted_items=listing_json.get("vaultedItems", None),
                    immutable_collection=listing_json.get("immutableCollection", None),
                    immutable_token_id=listing_json.get("immutableTokenId", None),
                    token_data=token_data.data,
                )
            )
        return listings

    def query_listing(self, cursor=""):
        try:
            params = {"collection": "all"}
            if cursor:
                params["cursor"] = cursor

            response = requests.get(self.URL, params=params).json()
            return response["listings"], response["cursor"]
        except Exception as e:
            logger.error(e)
        return [], None

    def save(self, listings):
        Listing.objects.bulk_create(listings, ignore_conflicts=True)

    def handle(self, query_limit=0):
        listings = []
        cursor = None
        for _ in range(query_limit or self.NESTED_QUERY_LIMIT):
            sub_listing, cursor = self.query_listing(cursor)

            print(self.decode_cursor(cursor))
            listings += self.serialize(sub_listing)
        self.save(listings)
