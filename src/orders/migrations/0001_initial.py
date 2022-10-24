# Generated by Django 4.1.2 on 2022-10-23 22:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("products", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
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
                    "code",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        max_length=12,
                        null=True,
                        unique=True,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        help_text="User who placed the order.",
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("-modified",),
            },
        ),
        migrations.CreateModel(
            name="OrderItem",
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
                ("quantity", models.IntegerField(default=1)),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="orders.order",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="orders",
                        to="products.product",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
