# Generated by Django 4.1.6 on 2023-02-22 14:32

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("aggregators", "0008_arcadeloanclaimed_arcadeloanrepaid_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="arcadeloanclaimed",
            name="amount",
        ),
        migrations.RemoveField(
            model_name="arcadeloanclaimed",
            name="to",
        ),
        migrations.RemoveField(
            model_name="arcadeloanclaimed",
            name="token",
        ),
    ]
