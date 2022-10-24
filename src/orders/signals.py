from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.models import OrderItem


@receiver(post_save, sender=OrderItem)
def update_product_stock(sender, instance, created, **kwargs):
    # Update product stock based on the quantity in the order.
    product = instance.product
    product.stock = product.stock - instance.quantity
    product.save()
