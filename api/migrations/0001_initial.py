# Generated by Django 4.1.7 on 2023-02-26 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

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
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, help_text="Thời gian cập nhật"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, help_text="Thời gian tạo"),
                ),
                ("name", models.CharField(max_length=100)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]