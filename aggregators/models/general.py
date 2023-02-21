from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


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
