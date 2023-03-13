# Generated by Django 4.1.7 on 2023-03-12 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0019_remove_sourcedata_key_words_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="key_words",
        ),
        migrations.AddField(
            model_name="product",
            name="source_description",
            field=models.CharField(default={}, max_length=250, null=True),
        ),
    ]
