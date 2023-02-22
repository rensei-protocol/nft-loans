from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import JSONField
from django.utils.translation import gettext_lazy as _

from aggregators.models.helper import MARKETPLACES
from nft_loans.configs.logger import logger


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
    amount = models.CharField(max_length=25)
    repayment = models.CharField(max_length=25)
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
        return round(duration / 86400, 1)

    def calculate_apr(self):
        try:
            profit = float(self.repayment) - float(self.amount)
            apr_ratio = profit / float(self.amount) / self.get_duration_in_days() * 365
            return round(apr_ratio * 100, 1)
        except Exception as e:
            logger.error(e)
            return -1

    def calculate_apr_arcade_by_set_repayment(self, interest_rate: str):
        try:
            amount = float(self.amount)
            decimals = pow(10, 22)
            repayment = (1 + float(interest_rate) / decimals) * amount
            self.repayment = str(repayment)
            return self.calculate_apr()
        except Exception as e:
            logger.error(e)
            return -1
