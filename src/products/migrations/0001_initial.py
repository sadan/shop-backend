# Generated by Django 4.1.2 on 2022-10-23 22:39

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
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.CharField(blank=True, max_length=128, null=True),
                ),
                (
                    "modified_by",
                    models.CharField(blank=True, max_length=128, null=True),
                ),
                (
                    "name",
                    models.CharField(help_text="Name of the product.", max_length=256),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="Price of the product e.g., 100.00.",
                        max_digits=5,
                    ),
                ),
                (
                    "stock",
                    models.IntegerField(
                        default=0,
                        help_text="Quantity of this product in stock.",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
