# Generated by Django 4.1.6 on 2023-02-22 11:29

import django.db.models.deletion
from django.db import migrations, models

import aggregators.models.general


class Migration(migrations.Migration):
    dependencies = [
        ("aggregators", "0007_rename_nftfioffers_nftfioffer"),
    ]

    operations = [
        migrations.RenameField(
            model_name="nftfioffer",
            old_name="date",
            new_name="create_time",
        ),
        migrations.RenameField(
            model_name="nftfioffer",
            old_name="lender_nonce",
            new_name="nonce",
        ),
        migrations.RemoveField(
            model_name="nftfioffer",
            name="loan",
        ),
        migrations.RemoveField(
            model_name="x2y2offer",
            name="nft_address",
        ),
        migrations.AddField(
            model_name="nftfioffer",
            name="amount",
            field=models.CharField(default="0", max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="nftfioffer",
            name="apr",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="nftfioffer",
            name="duration",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="nftfioffer",
            name="erc20_address",
            field=models.CharField(
                default="0x",
                max_length=44,
                validators=[aggregators.models.general.validate_address],
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="nftfioffer",
            name="expire_time",
            field=models.DateTimeField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="nftfioffer",
            name="repayment",
            field=models.CharField(default="", max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="x2y2offer",
            name="collection",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="aggregators.collection",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="nftfioffer",
            name="lender",
            field=models.CharField(
                max_length=44, validators=[aggregators.models.general.validate_address]
            ),
        ),
        migrations.AlterField(
            model_name="x2y2offer",
            name="amount",
            field=models.CharField(default="0", max_length=25),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="x2y2offer",
            name="apr",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name="x2y2offer",
            name="create_time",
        ),
        migrations.AddField(
            model_name="x2y2offer",
            name="create_time",
            field=models.DateTimeField(default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="x2y2offer",
            name="duration",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="x2y2offer",
            name="erc20_address",
            field=models.CharField(
                default=None,
                max_length=44,
                validators=[aggregators.models.general.validate_address],
            ),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name="x2y2offer",
            name="expire_time",
        ),
        migrations.AddField(
            model_name="x2y2offer",
            name="expire_time",
            field=models.DateTimeField(default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="x2y2offer",
            name="lender",
            field=models.CharField(
                max_length=44, validators=[aggregators.models.general.validate_address]
            ),
        ),
        migrations.AlterField(
            model_name="x2y2offer",
            name="repayment",
            field=models.CharField(max_length=25),
        ),
    ]