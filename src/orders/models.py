from django.conf import settings
from django.db import models
from django.utils.crypto import get_random_string

from base.models import BaseModel
from products.models import Product


class Order(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text="User who placed the order.",
    )
    code = models.CharField(
        max_length=12, unique=True, db_index=True, null=True, blank=True
    )

    class Meta:
        ordering = ("-modified",)

    # TODO: order_status

    def __str__(self) -> str:
        return self.code

    def save(self, *args, **kwargs):
        # For newly created records, generate the code
        if not self.id and not self.code:
            self.code = self._random_code_generator()

        return super().save(*args, **kwargs)

    def _random_code_generator(self):
        # TODO: length should be configurable.
        code = get_random_string(length=12)
        try:
            self._meta.model.objects.get(code=code)
        except self._meta.model.DoesNotExist:
            return code


class OrderItem(BaseModel):
    product = models.ForeignKey(
        Product, related_name="orders", on_delete=models.CASCADE
    )
    order = models.ForeignKey("Order", related_name="items", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, null=False)

    @property
    def total(self):
        return self.product.price * self.quantity
