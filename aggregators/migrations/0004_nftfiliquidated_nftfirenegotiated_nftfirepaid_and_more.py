# Generated by Django 4.1.6 on 2023-02-16 13:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("aggregators", "0003_alter_arcadeloan_block_number_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="NftfiLiquidated",
            fields=[
                (
                    "block_number",
                    models.IntegerField(blank=True, db_index=True, null=True),
                ),
                ("block_time", models.DateTimeField(blank=True, null=True)),
                ("borrower", models.TextField(blank=True, null=True)),
                ("lender", models.CharField(blank=True, max_length=100, null=True)),
                ("loan_id", models.IntegerField(primary_key=True, serialize=False)),
                ("loan_liquidation_date", models.DateTimeField(blank=True, null=True)),
                ("loan_maturity_date", models.DateTimeField(blank=True, null=True)),
                ("loan_principal_amount", models.TextField(blank=True, null=True)),
                ("nft_collateral_contract", models.TextField(blank=True, null=True)),
                ("nft_collateral_id", models.TextField(blank=True, null=True)),
                ("transaction_hash", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="NftfiRenegotiated",
            fields=[
                (
                    "block_number",
                    models.IntegerField(blank=True, db_index=True, null=True),
                ),
                ("block_time", models.DateTimeField(blank=True, null=True)),
                ("borrower", models.TextField(blank=True, null=True)),
                ("lender", models.CharField(blank=True, max_length=100, null=True)),
                ("loan_id", models.IntegerField(primary_key=True, serialize=False)),
                ("new_loan_duration", models.TextField(blank=True, null=True)),
                (
                    "new_maximum_repayment_amount",
                    models.TextField(blank=True, null=True),
                ),
                ("renegotiation_admin_fee", models.TextField(blank=True, null=True)),
                ("renegotiation_fee", models.TextField(blank=True, null=True)),
                ("transaction_hash", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="NftfiRepaid",
            fields=[
                ("admin_fee", models.TextField(blank=True, null=True)),
                ("amount_paid_to_lender", models.TextField(blank=True, null=True)),
                (
                    "block_number",
                    models.IntegerField(blank=True, db_index=True, null=True),
                ),
                ("block_time", models.DateTimeField(blank=True, null=True)),
                ("borrower", models.TextField(blank=True, null=True)),
                ("lender", models.CharField(blank=True, max_length=100, null=True)),
                ("loan_erc20_denomination", models.TextField(blank=True, null=True)),
                ("loan_id", models.IntegerField(primary_key=True, serialize=False)),
                ("loan_principal_amount", models.TextField(blank=True, null=True)),
                ("nft_collateral_contract", models.TextField(blank=True, null=True)),
                ("nft_collateral_id", models.TextField(blank=True, null=True)),
                (
                    "revenue_share",
                    models.CharField(blank=True, max_length=30, null=True),
                ),
                ("revenue_share_partner", models.TextField(blank=True, null=True)),
                ("transaction_hash", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.RenameField(
            model_name="benddaoborrow",
            old_name="block_timestamp",
            new_name="block_time",
        ),
        migrations.RenameField(
            model_name="benddaoliquidate",
            old_name="block_timestamp",
            new_name="block_time",
        ),
        migrations.RenameField(
            model_name="benddaoredeem",
            old_name="block_timestamp",
            new_name="block_time",
        ),
    ]
