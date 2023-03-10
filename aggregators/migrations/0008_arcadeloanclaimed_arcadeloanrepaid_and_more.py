# Generated by Django 4.1.6 on 2023-02-22 14:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("aggregators", "0007_rename_nftfioffers_nftfioffer"),
    ]

    operations = [
        migrations.CreateModel(
            name="ArcadeLoanClaimed",
            fields=[
                ("loan_id", models.IntegerField(primary_key=True, serialize=False)),
                ("token", models.TextField(blank=True, null=True)),
                ("to", models.TextField(blank=True, null=True)),
                ("amount", models.TextField(blank=True, null=True)),
                ("block_number", models.IntegerField(blank=True, null=True)),
                ("block_time_stamp", models.DateTimeField(blank=True, null=True)),
                ("transaction_hash", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="ArcadeLoanRepaid",
            fields=[
                ("loan_id", models.IntegerField(primary_key=True, serialize=False)),
                ("block_number", models.IntegerField(blank=True, null=True)),
                ("block_time_stamp", models.DateTimeField(blank=True, null=True)),
                ("transaction_hash", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="ArcadeLoanRolledOver",
            fields=[
                ("old_loan_id", models.IntegerField(primary_key=True, serialize=False)),
                ("new_loan_id", models.IntegerField()),
                ("block_number", models.IntegerField(blank=True, null=True)),
                ("block_time_stamp", models.DateTimeField(blank=True, null=True)),
                ("transaction_hash", models.TextField(blank=True, null=True)),
            ],
        ),
    ]
