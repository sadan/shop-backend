from rest_framework import routers

from products.views import ProductsViewSet

router = routers.SimpleRouter()
router.register(r"products", ProductsViewSet, basename="product")
urlpatterns = router.urls
