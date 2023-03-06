# Generated by Django 4.1.7 on 2023-03-05 18:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0005_producttest_delete_product"),
    ]

    operations = [
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
                ("name", models.CharField(default={}, max_length=250, null=True)),
                ("price", models.CharField(default={}, max_length=250, null=True)),
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
                ("describe", models.CharField(default={}, max_length=250, null=True)),
                ("min_page", models.IntegerField(null=True)),
                ("max_page", models.IntegerField(null=True)),
                ("multi_page", models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name="producttest",
            name="image_path",
            field=models.CharField(default={}, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="producttest",
            name="name",
            field=models.CharField(default={}, max_length=250, null=True),
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
