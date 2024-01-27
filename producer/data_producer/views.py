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


class ChangeOrderStatusView(APIView):
    queryset = Order.objects.all()
    serializer_class = OrderUpdateSerializer
    permission_classes = [IsAuthenticated, HasAPIKey]

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
