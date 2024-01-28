import decimal
from django.db.models import Sum
from django.core.exceptions import ValidationError
from users.models import CustomUser
from rest_framework import serializers
from .models import Order, OrderItem
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone
from .models import TaskResult


class TaskResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskResult
        fields = ["task_id", "result"]


class OrderItemGetSerializer(serializers.ModelSerializer):
    """Serializer for Getting OrderItem"""

    class Meta:
        model = OrderItem
        fields = (
            "item_name",
            "price",
            "quantity",
        )


class OrderItemPostSerializer(serializers.ModelSerializer):
    """Serializer for HTTP Methods OrderItem"""

    class Meta:
        model = OrderItem
        fields = (
            "item_name",
            "price",
            "quantity",
        )


class OrderSerializer(serializers.ModelSerializer):
    """SerializerAbstract for Order"""

    class Meta:
        model = Order
        fields = (
            "uuid",
            "user",
            "address",
            "phone_number",
            "created_at",
            "total_paid",
            "order_key",
            "status",
            "currency",
            "items",
        )
        read_only_fields = (
            "uuid",
            "created_at",
            "updated_at",
            "order_key",
            "user",
            "status",
        )


class OrderGetSerializer(OrderSerializer):
    """Serializer for Getting Order"""

    items = OrderItemGetSerializer(many=True)


class OrderPostSerializer(OrderSerializer):
    """Serializer for Posting Order"""

    items = OrderItemPostSerializer(many=True)

    def create(self, validated_data):
        """
        Create an Order object from serializer
        """
        orderItems_list = validated_data.pop("items", None)
        user = self.context["request"].user

        if user:

            order_code = Order._generate_order_code(user)
            order = Order.objects.create(
                user=user,
                order_key=order_code,
                **validated_data,
            )
            order.save()

            phone_number = user.phone_number
            if phone_number:
                order.phone_number = phone_number
            order.save()

            if orderItems_list:
                for orderItem in orderItems_list:
                    OrderItem.objects.create(
                        order=order,
                        item_name=orderItem["item_name"],
                        price=orderItem["price"],
                        quantity=orderItem["quantity"],
                    )
            order.save()
            return order

    def update(self, instance, validated_data):
        """
        Update PUT and PATCH for order object
        """
        instance.status = validated_data.get("status", instance.status)
        instance.save()

        return instance


class OrderUpdateSerializer(serializers.Serializer):
    taskId = serializers.CharField()
    status = serializers.CharField()
