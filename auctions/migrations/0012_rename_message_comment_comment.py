# Generated by Django 5.0 on 2023-12-26 22:06

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0011_rename_bid_bid_price_rename_price_listing_bid"),
    ]

    operations = [
        migrations.RenameField(
            model_name="comment",
            old_name="message",
            new_name="comment",
        ),
    ]