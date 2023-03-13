from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import JSONField
from django.utils.translation import gettext_lazy as _

from aggregators.models.helper import (
    MARKETPLACES,
    CURRENCY_METADATA_SOURCE,
    NOTABENE,
    NETWORKS_CHOICES,
)
from nft_loans.configs.logger import logger


class CurrencyMetadata(models.Model):
    address = models.CharField(max_length=44, primary_key=True)
    symbol = models.CharField(max_length=15, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    decimals = models.IntegerField(null=True, blank=True)
    network = models.CharField(
        max_length=20, null=True, blank=True, choices=NETWORKS_CHOICES
    )
    source = models.CharField(
        max_length=15, choices=CURRENCY_METADATA_SOURCE, default=NOTABENE
    )


def validate_address(value):
    if value[:2] != "0x":
        raise ValidationError(
            _("%(value)s is not a valid collection address"),
            params={"value": value},
        )


class Collection(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(
        max_length=44, validators=[validate_address], primary_key=True
    )

    @classmethod
    def get_all_collections(cls):
        return cls.objects.all().values_list("address", flat=True)

    def save(self, *args, **kwargs):
        self.address = self.address.lower()
        return super().save(*args, **kwargs)


class CollectionOffer(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    marketplace = models.CharField(max_length=15, choices=MARKETPLACES)
    apr = models.FloatField()
    amount = models.FloatField()  # amount as string 2e18
    repayment = models.FloatField()
    expire_time = models.DateTimeField()
    duration = models.IntegerField()
    erc20_address = models.CharField(max_length=44, validators=[validate_address])
    lender = models.CharField(max_length=44, validators=[validate_address])
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    create_time = models.DateTimeField()
    nonce = models.TextField(blank=True, null=True)
    signature = models.TextField(blank=True, null=True)
    x2y2_metadata = JSONField(null=True, blank=True)
    nftfi_metadata = JSONField(null=True, blank=True)
    arcade_metadata = JSONField(null=True, blank=True)

    fee = models.FloatField()
    currency = models.ForeignKey(
        CurrencyMetadata, on_delete=models.SET_NULL, null=True, blank=True
    )

    _YEAR = 365
    _DAY_IN_SEC = 86400

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["id", "marketplace"], name="unique_id_and_marketplace"
            )
        ]

    @classmethod
    def get_metadata_fieldnames(cls):
        return ["x2y2_metadata", "nftfi_metadata", "arcade_metadata"]

    def get_duration_in_days(self):
        duration = self.duration or 0
        return round(duration / self._DAY_IN_SEC, 3)

    def calculate_apr(self):
        try:
            profit = float(self.repayment) - float(self.amount)
            apr_ratio = (
                profit / float(self.amount) / self.get_duration_in_days() * self._YEAR
            )
            return round(apr_ratio * 100, 3)
        except Exception as e:
            logger.error(e)
            return -1

    def calculate_apr_arcade_by_set_repayment(self, interest_rate: str):
        try:
            decimals = pow(10, 22)
            repayment = (1 + float(interest_rate) / decimals) * self.amount
            self.repayment = repayment
            return self.calculate_apr()
        except Exception as e:
            logger.error(e)
            return -1

    def _set_currency(self):
        if self.currency:
            return
        try:
            self.currency = CurrencyMetadata.objects.get(
                address__iexact=self.erc20_address.lower()
            )
        except:
            logger.error(f"{self.erc20_address} does not exist in db!")

    def _set_fee(self):
        try:
            self.fee = self.repayment - self.amount
        except Exception as e:
            logger.error(f"Error in setting fee of offer: {e}")

    def set_essentials(self):
        self._set_currency()
        self._set_fee()


class Listing(models.Model):
    marketplace = models.CharField(max_length=15, choices=MARKETPLACES)
    listing_id = models.TextField(primary_key=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    token_id = models.CharField(max_length=50)
    borrower = models.CharField(max_length=44)
    listed_at = models.DateTimeField()
    desired_terms = JSONField()
    borrower_stats = JSONField()
    vaulted_items = JSONField(null=True, blank=True)
    immutable_collection = models.CharField(max_length=44, null=True, blank=True)
    immutable_token_id = models.TextField(null=True, blank=True)
    token_data = JSONField(null=True, blank=True)
