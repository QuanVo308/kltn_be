# Generated by Django 4.1.7 on 2023-03-08 19:24

from django.db import migrations
import djongo.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0017_sourcedata_key_words"),
    ]

    operations = [
        migrations.AddField(
            model_name="image",
            name="embedding_vector",
            field=djongo.models.fields.JSONField(default=[], null=True),
        ),
    ]