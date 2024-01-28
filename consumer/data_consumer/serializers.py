from rest_framework import serializers


class OrderSerializer(serializers.Serializer):
    webhook_url = serializers.CharField()
    address = serializers.CharField()
    phone_number = serializers.CharField()
    order_key = serializers.CharField()
    status = serializers.CharField()
    currency = serializers.CharField()


class TaskResultSerializer(serializers.Serializer):
    task_id = serializers.UUIDField()
    result = serializers.CharField()
