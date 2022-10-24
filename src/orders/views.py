from rest_framework import mixins, viewsets

from orders.models import Order
from orders.serializers import OrderSerializer


class OrderViewset(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = OrderSerializer
    lookup_field = "order_id"

    # If DEFAULT_PAGINATION_CLASS is provided in settings ListModelMixin will
    # return a paginated response. Uncomment following line to disable
    # pagination for this viewset.
    # pagination_class = None

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
