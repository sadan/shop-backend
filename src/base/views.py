from django.utils import timezone

from rest_framework.response import Response
from rest_framework.views import APIView


class HealthAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response({"status": "OK", "timestamp": timezone.now()})
