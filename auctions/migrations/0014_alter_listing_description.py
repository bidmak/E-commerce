# Generated by Django 5.0 on 2023-12-28 23:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0013_rename_categoryname_category_category_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listing",
            name="description",
            field=models.CharField(max_length=300),
        ),
    ]
