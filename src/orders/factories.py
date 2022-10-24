import factory
from django.db.models.signals import post_save
from factory import fuzzy
from factory.django import DjangoModelFactory

from base.factories import UserFactory
from orders.models import Order, OrderItem
from products.factories import ProductFactory


class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)
    code = fuzzy.FuzzyText(length=12)


@factory.django.mute_signals(post_save)
class OrderItemFactory(DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory, **{"stock": 10})
    quantity = fuzzy.FuzzyInteger(1, 10)
