# Generated by Django 4.1.7 on 2023-03-06 18:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0009_product_link"),
    ]

    operations = [
        migrations.RenameField(
            model_name="sourcedata",
            old_name="describe",
            new_name="description",
        ),
    ]