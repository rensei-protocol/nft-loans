import os

import requests

from aggregators.models import Collection
from aggregators.serializers import NFTScanMetadataSerializer
from nft_loans.configs.logger import logger


class NftscanMetadataFetcher:
    API_KEY = os.getenv("NFTSCAN_KEY")
    url = "https://restapi.nftscan.com/api/v2/account/own/all/{owner}"

    @classmethod
    def get_supported_nfts(self, raw_nfts):
        supported_collections = Collection.get_all_collections()
        return [
            col
            for col in raw_nfts
            if col["contract_address"].lower() in supported_collections
        ]

    @classmethod
    def serialize(self, raw_nfts):
        ser = NFTScanMetadataSerializer(data=raw_nfts, many=True)
        ser.is_valid()
        return ser.data

    @classmethod
    def fetch_nfts_by_owner(cls, owner: str):
        try:
            header = {"X-API-KEY": cls.API_KEY}
            params = {"show_attribute": False, "erc_type": ""}
            raw_nfts = requests.get(
                cls.url.format(owner=owner), headers=header, params=params
            ).json()["data"]
            supported_nfts = cls.get_supported_nfts(raw_nfts)
            nfts = cls.serialize(raw_nfts=supported_nfts)
            return nfts
        except Exception as e:
            logger.error(e)
        return []
