import requests
from django.db import transaction

from aggregators.models import CurrencyMetadata
from aggregators.models.helper import SUPPORTED_NETWORKS, NOTABENE
from nft_loans.configs.logger import logger


class CurrencyCoingeckoFetcher:
    url = "https://assets.notabene.id/assets"
    batch_size = 500

    def serialize(self, raw_currencies):
        currencies = []
        for raw_currency in raw_currencies:
            try:
                if raw_currency.get("notabene_network", "") not in SUPPORTED_NETWORKS:
                    continue
                address = raw_currency["asset_type"].split(":")[-1].lower()
                if address[:2] != "0x":
                    continue
                currencies.append(
                    CurrencyMetadata(
                        address=address,
                        symbol=raw_currency["notabene_asset"],
                        name=raw_currency["notabene_description"],
                        decimals=raw_currency["decimals"],
                        network=raw_currency["notabene_network"],
                        source=NOTABENE,
                    )
                )
            except:
                continue
        return currencies

    def fetch(self):
        try:
            raw_currencies = requests.get(self.url).json()
            currencies = self.serialize(raw_currencies["data"])

            if len(currencies) == 0:
                logger.error(f"[CurrencyCoingeckoFetcher] no currencies!")
                return

            with transaction.atomic():
                # CurrencyMetadata.objects.all().delete()
                CurrencyMetadata.objects.bulk_create(
                    currencies,
                    batch_size=self.batch_size,
                    ignore_conflicts=True,
                )
                logger.info(f"[CurrencyCoingeckoFetcher] all currencies are updated!")

        except Exception as e:
            logger.error(e)
