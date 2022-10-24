from rest_framework import routers

from orders.views import OrderViewset

router = routers.SimpleRouter()
router.register(r"orders", OrderViewset, basename="order")
urlpatterns = router.urls
