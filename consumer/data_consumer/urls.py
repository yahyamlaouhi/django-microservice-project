from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProcessMessageView, SendMessageView, TaskResultViewSet

router = DefaultRouter()
router.register("tasks", TaskResultViewSet)

urlpatterns = [
    path("send-message/", SendMessageView.as_view(), name="send_message"),
    path("process-message/", ProcessMessageView.as_view(), name="process_message"),
    path("", include(router.urls)),
]
