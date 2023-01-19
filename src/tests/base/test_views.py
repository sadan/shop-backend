from django.urls import reverse


class TestHealthAPIView:
    def test_get(self, client):
        response = client.get(reverse("health"))
        assert response.json()["status"] == "OK"
