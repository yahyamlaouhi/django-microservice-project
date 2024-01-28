from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes
from .tasks import change_status_data, process_data
from .serializers import OrderSerializer, TaskResultSerializer
from django_celery_results.models import TaskResult
from rest_framework import viewsets
from rest_framework_api_key.models import APIKey
from rest_framework_api_key.permissions import HasAPIKey


class SendMessageView(APIView):
    def post(self, request, *args, **kwargs):

        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():

            webhook_url = serializer.data.get("webhook_url")
            status = serializer.data.get("status")

        if not all([status, webhook_url]):
            return Response({"error": "Missing data"}, status=400)

        change_status_data.delay(serializer.data, webhook_url)

        return Response({"status": "Task started"})


class ProcessMessageView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            status = serializer.data.get("status")
            currency = serializer.data.get("currency")
            order_key = serializer.data.get("order_key")

        if not all([status, currency, order_key]):
            return Response({"error": "Missing data"}, status=400)

        process_data.delay(status, currency, order_key)

        return Response({"status": "Task started"})


# task 8
class TaskResultViewSet(viewsets.ModelViewSet):
    queryset = TaskResult.objects.all()
    serializer_class = TaskResultSerializer
    permission_classes = [HasAPIKey]
