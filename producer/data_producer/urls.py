from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, ChangeOrderStatusView

router = DefaultRouter()
router.register("orders", OrderViewSet)

app_name = "orders"

urlpatterns = [
    path("/", include(router.urls)),
    path(
        "/orders/<uuid:uuid>/status/update",
        ChangeOrderStatusView.as_view(),
        name="change_order_status",
    ),
]
