# orders/tests/test_models.py
from django.test import TestCase
from .models import Order, OrderItem, OrderAPIKey, TaskResult
from users.models import CustomUser
from django.utils import timezone
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.conf import settings


class OrderModelTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = CustomUser.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )

    def test_order_creation(self):
        order = Order.objects.create(
            user=self.user,
            address="Test Address",
            phone_number="+123456789",
            created_at=timezone.now(),
            total_paid=50,
            currency="USD",
            order_key="TestOrderKey",
            status="pending",
        )

        self.assertEqual(order.status, "pending")
        self.assertEqual(str(order), "TestOrderKey")

class OrderItemModelTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = CustomUser.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )

        # Create an order for testing
        self.order = Order.objects.create(
            user=self.user,
            address="Test Address",
            phone_number="+123456789",
            created_at=timezone.now(),
            total_paid=50,
            currency="USD",
            order_key="TestOrderKey",
            status="pending",
        )

    def test_order_item_creation(self):
        order_item = OrderItem.objects.create(
            order=self.order,
            item_name="TestItem",
            price=25,
            quantity=2,
        )

        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(str(order_item), "1 TestItem")




class OrderViewSetTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )
        self.client = APIClient()

    def test_create_order_without_authentication(self):
        url = reverse("orders:order-list")
        data = {
            "user": self.user.id,
            "address": "Test Address",
            "phone_number": "+123456789",
            "total_paid": 50,
            "currency": "USD",
            "items": [{"item_name": "item1", "price": 20, "quantity": 1}],
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



class OrderViewSetTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )
        self.client = APIClient()

    def test_create_order_without_authentication(self):
        url = reverse("orders:order-list")
        data = {
            "user": self.user.id,
            "address": "Test Address",
            "phone_number": "+123456789",
            "total_paid": 50,
            "currency": "USD",
            "items": [{"item_name": "item1", "price": 20, "quantity": 1}],
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_order_with_authentication(self):
        self.client.force_authenticate(user=self.user)

        url = reverse("orders:order-list")
        data = {
            "user": self.user.id,
            "address": "Ariana Nkhilet",
            "phone_number": "+21658741196",
            "total_paid": 50,
            "currency": "TND",
            "items": [{"item_name": "item1", "price": 20, "quantity": 1}],
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class ChangeOrderStatusViewTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )
        self.order = Order.objects.create(
            user=self.user,
            address="Test Address",
            phone_number="+123456789",
            created_at=timezone.now(),
            total_paid=50,
            currency="USD",
            order_key="TestOrderKey",
            status="pending",
        )
        self.client = APIClient()


    def test_change_order_status_without_api_authorization(self):
        url = reverse("orders:change_order_status", args=[str(self.order.uuid)])
        data = {"status": "invalid_status"}

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

