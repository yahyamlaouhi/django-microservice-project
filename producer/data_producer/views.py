from .serializers import (
    OrderSerializer,
    OrderGetSerializer,
    OrderPostSerializer,
    OrderUpdateSerializer,
)
from .models import Order, OrderItem
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_api_key.models import APIKey
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .utils import send_request
import requests
from .models import TaskResult
from .serializers import TaskResultSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """Manage Orders in the database"""

    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    lookup_field = "uuid"
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return OrderGetSerializer
        else:
            return OrderPostSerializer

    def perform_create(self, serializer):
        # Save the order
        order = serializer.save()

        # Send a request to an API after creating the order
        response = send_request(order)

        if response.status_code == 200:
            print("Request to API successful!")
        else:
            print(f"Request to API failed. Status code: {response.status_code}")


class ChangeOrderStatusView(APIView):
    queryset = Order.objects.all()
    serializer_class = OrderUpdateSerializer
    permission_classes = [HasAPIKey]

    def post(self, request, *args, **kwargs):
        uuid = self.kwargs.get("uuid")
        order = Order.objects.get(uuid=uuid)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_status = serializer.validated_data.get("status")

        if order and new_status:
            order.status = new_status
            order.save()

            return Response(
                {"the new status ": new_status}, status=status.HTTP_201_CREATED
            )

        return Response(
            {"error": "Invalid data format"}, status=status.HTTP_400_BAD_REQUEST
        )


class TaskResultViewSet(viewsets.ModelViewSet):
    queryset = TaskResult.objects.all()
    serializer_class = TaskResultSerializer
    permission_classes = (IsAuthenticated,)

