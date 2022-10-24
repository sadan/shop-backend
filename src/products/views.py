from rest_framework import pagination, viewsets

from products.models import Product
from products.serializers import ProductSerializer


class ProductsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = pagination.PageNumberPagination
