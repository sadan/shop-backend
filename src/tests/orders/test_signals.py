from orders.factories import OrderItemFactory
from orders.models import OrderItem
from orders.signals import update_product_stock


class TestOrderSignals:
    def test_update_product_stock(self, db, django_db_setup):
        quantity = 2
        order_item = OrderItemFactory(quantity=quantity)
        product = order_item.product
        updated_stock = product.stock - quantity
        signal = update_product_stock(OrderItem, order_item, True)
        assert signal is None
        assert product.stock == updated_stock
