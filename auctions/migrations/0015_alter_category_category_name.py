# Generated by Django 5.0 on 2023-12-28 23:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0014_alter_listing_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="category_name",
            field=models.CharField(max_length=30),
        ),
    ]
