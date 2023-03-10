# Generated by Django 4.1.6 on 2023-03-03 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("aggregators", "0012_currencymetadata"),
    ]

    operations = [
        migrations.AddField(
            model_name="collectionoffer",
            name="currency",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="aggregators.currencymetadata",
            ),
        ),
        migrations.AddField(
            model_name="collectionoffer",
            name="fee",
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="collectionoffer",
            name="amount",
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name="collectionoffer",
            name="repayment",
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name="currencymetadata",
            name="network",
            field=models.CharField(
                blank=True, choices=[("ethereum", "ethereum")], max_length=20, null=True
            ),
        ),
    ]
