# Generated by Django 4.1.7 on 2023-04-04 17:50

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name="ProductTest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(default={}, max_length=250, null=True)),
                ("image_url", models.CharField(default={}, max_length=250, null=True)),
                ("image_path", models.CharField(default={}, max_length=250, null=True)),
                (
                    "embedding_vector",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.FloatField(), default=[], size=None
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, help_text="Thời gian cập nhật"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, help_text="Thời gian tạo"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SourceData",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("platform", models.CharField(default={}, max_length=250, null=True)),
                ("link", models.CharField(default={}, max_length=250, null=True)),
                (
                    "description",
                    models.CharField(default={}, max_length=250, null=True),
                ),
                ("crawled", models.BooleanField(default=False)),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, help_text="Thời gian cập nhật"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, help_text="Thời gian tạo"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(default="", max_length=250, null=True)),
                ("price", models.CharField(default="", max_length=250, null=True)),
                ("link", models.CharField(default="", max_length=250, null=True)),
                (
                    "source_description",
                    models.CharField(default={}, max_length=250, null=True),
                ),
                ("crawled", models.BooleanField(default=False)),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, help_text="Thời gian cập nhật"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, help_text="Thời gian tạo"),
                ),
                (
                    "category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="products",
                        to="api.category",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("link", models.CharField(default={}, max_length=250, null=True)),
                (
                    "embedding_vector",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.FloatField(), default=[], size=None
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, help_text="Thời gian cập nhật"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, help_text="Thời gian tạo"),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="api.product",
                    ),
                ),
            ],
        ),
    ]
