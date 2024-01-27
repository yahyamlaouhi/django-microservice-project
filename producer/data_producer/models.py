import uuid
from django.db import models
from users.models import CustomUser
from .utils import get_upper_first_three_letters
import datetime
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework_api_key.models import AbstractAPIKey


class Order(models.Model):
    """Order model to be created by customer and consulted by restaurent"""

    STATUS = [
        ("pending", "pending"),
        ("confirmed", "confirmed"),
        ("cancelled", "cancelled"),
    ]

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="order_user"
    )
    address = models.CharField(max_length=100, blank=True)

    phone_number = PhoneNumberField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True, null=True)

    total_paid = models.DecimalField(max_digits=5, decimal_places=2)

    currency = models.CharField(max_length=20, default=settings.CURRENCY["tunisia"])

    order_key = models.CharField(max_length=100, unique=True)

    status = models.CharField(max_length=50, choices=STATUS, default="pending")

    def __init__(self, *args, **kwargs):
        super(Order, self).__init__(*args, **kwargs)
        self.old_status = self.status

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return str(self.order_key)

    @staticmethod
    def _generate_order_code(customer):
        """
        generate order_code for each new order
        """

        user_code = get_upper_first_three_letters(
            "".join([c for c in customer.email.split("@")[0] if c.isalpha()])
        )
        order_date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        order_code = f"{user_code}{order_date}"
        return order_code


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    item_name = models.CharField(max_length=50, default="item")
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.id} {self.item_name}"


class OrderAPIKey(AbstractAPIKey):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="api_keys",
    )
