# Generated by Django 4.1.7 on 2023-03-07 17:22

from django.db import migrations
import djongo.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0012_sourcedata_key_words"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="key_words",
            field=djongo.models.fields.JSONField(default={}, null=True),
        ),
    ]
