from django.core.management.base import BaseCommand

from products.factories import ProductFactory


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        ProductFactory.create_batch(size=20)
