# Generated by Django 4.1.7 on 2023-04-13 14:27

from django.db import migrations
import djongo.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0029_producttest_embedding_vector_rembg"),
    ]

    operations = [
        migrations.AddField(
            model_name="image",
            name="embedding_vector_temp",
            field=djongo.models.fields.JSONField(default=[], null=True),
        ),
    ]
