# Generated by Django 4.1.6 on 2023-03-13 10:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("aggregators", "0013_collectionoffer_currency_collectionoffer_fee_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Listing",
            fields=[
                (
                    "marketplace",
                    models.CharField(
                        choices=[
                            ("nftfi", "nftfi"),
                            ("x2y2", "x2y2"),
                            ("arcade", "arcade"),
                            ("bendao", "bendao"),
                        ],
                        max_length=15,
                    ),
                ),
                ("listing_id", models.TextField(primary_key=True, serialize=False)),
                ("token_id", models.CharField(max_length=50)),
                ("borrower", models.CharField(max_length=44)),
                ("listed_at", models.DateTimeField()),
                ("desired_terms", models.JSONField()),
                ("borrower_stats", models.JSONField()),
                ("vaulted_items", models.JSONField(blank=True, null=True)),
                (
                    "immutable_collection",
                    models.CharField(blank=True, max_length=44, null=True),
                ),
                (
                    "immutable_token_id",
                    models.CharField(blank=True, max_length=44, null=True),
                ),
                ("token_data", models.JSONField(blank=True, null=True)),
                (
                    "collection",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="aggregators.collection",
                    ),
                ),
            ],
        ),
    ]
