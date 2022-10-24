from django.db import models

from base.models import BaseModel


class Product(BaseModel):
    name = models.CharField(max_length=256, help_text="Name of the product.")
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Price of the product e.g., 100.00.",
    )
    stock = models.IntegerField(
        null=False,
        default=0,
        help_text="Quantity of this product in stock.",
    )

    def __str__(self) -> str:
        return f"{self.name} | {self.price}"
