from django.db import transaction

from rest_framework import serializers
from rest_framework_simplejwt.exceptions import InvalidToken

from orders.models import Order, OrderItem
from products.models import Product
from products.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)
    product = ProductSerializer(read_only=True)
    total = serializers.CharField(read_only=True)

    class Meta:
        model = OrderItem
        fields = ("product_id", "product", "quantity", "total")

    def validate_product_id(self, value):
        if value.stock > 0:
            return value.id
        raise serializers.ValidationError(f"{value.name} is out of stock.")


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ("user", "code", "items")
        read_only_fields = ("code",)
        extra_kwargs = {"user": {"required": False}}
        # depth = 1

    def validate(self, attrs):
        user = self.context.get("request").user

        if not user.is_authenticated:
            raise InvalidToken()

        attrs["user"] = user
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        items = validated_data.pop("items")

        # Create order.
        order = self.Meta.model.objects.create(**validated_data)

        # Create OrderProduct(s).
        for item in items:
            OrderItem.objects.create(order=order, **item)

        return order
