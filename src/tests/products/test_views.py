from django.urls import reverse

import pytest
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from base.factories import UserFactory
from products.factories import ProductFactory


class TestProductsViewSet:
    @pytest.fixture()
    def user(self, db, django_db_setup):
        return UserFactory()

    def call_endpoint(
        self,
        client,
        user,
        product_id=None,
        method="get",
    ):
        refresh = RefreshToken.for_user(user)
        kwargs = {"HTTP_AUTHORIZATION": f"Bearer {refresh.access_token}"}

        if product_id:
            endpoint = reverse("product-detail", kwargs={"pk": product_id})
        else:
            endpoint = reverse("product-list")

        return getattr(client, method)(path=endpoint, **kwargs)

    def test_list_successful(self, client, user, db, django_db_setup):
        ProductFactory.create_batch(size=15)
        response = self.call_endpoint(client=client, user=user)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["count"] == 15
        assert response.json()["next"]
        assert len(response.json()["results"]) == 10

    def test_retrieve_successful(self, client, user, db, django_db_setup):
        product = ProductFactory()
        response = self.call_endpoint(client=client, user=user, product_id=product.id)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == product.id
        assert response.json()["name"] == product.name
