from unittest import mock

from orders.factories import OrderFactory


class TestOrderModel:
    def test_order_created_generate_random_code(self, db, django_db_setup):
        order = OrderFactory()
        assert order.code

    @mock.patch("orders.models.Order._random_code_generator")
    def test_order_updated_does_not_update_code(self, random_code_generator, db, django_db_setup):
        order = OrderFactory()
        code = order.code

        order.save()
        assert order.code == code
        random_code_generator.assert_not_called()
