# Generated by Django 5.0 on 2023-12-26 20:27

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0010_listing_userbid"),
    ]

    operations = [
        migrations.RenameField(
            model_name="bid",
            old_name="bid",
            new_name="price",
        ),
        migrations.RenameField(
            model_name="listing",
            old_name="price",
            new_name="bid",
        ),
    ]
