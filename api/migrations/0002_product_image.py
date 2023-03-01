# Generated by Django 4.1.7 on 2023-02-26 17:05

from django.db import migrations, models
import djongo.storage


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="image",
            field=models.ImageField(
                null=True,
                storage=djongo.storage.GridFSStorage(
                    base_url="localhost:8000myfiles/", collection="myfiles"
                ),
                upload_to="testImage",
            ),
        ),
    ]
