import factory
from factory import fuzzy
from factory.django import DjangoModelFactory

from products.models import Product


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: "Product %02d" % n)
    price = fuzzy.FuzzyDecimal(0.5, 999.99)
    stock = fuzzy.FuzzyInteger(0, 100)
