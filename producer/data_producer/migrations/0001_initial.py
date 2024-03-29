# Generated by Django 3.2 on 2024-01-26 17:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("address", models.CharField(blank=True, max_length=100)),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True, max_length=128, null=True, region=None
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("total_paid", models.DecimalField(decimal_places=2, max_digits=5)),
                ("regular_price", models.DecimalField(decimal_places=2, max_digits=5)),
                ("currency", models.CharField(default="TND", max_length=20)),
                ("order_key", models.CharField(max_length=100, unique=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "pending"),
                            ("confirmed", "confirmed"),
                            ("cancelled", "cancelled"),
                        ],
                        default="received",
                        max_length=50,
                    ),
                ),
                (
                    "User",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="order_customer",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at",),
            },
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("item_name", models.CharField(default="item", max_length=50)),
                ("price", models.DecimalField(decimal_places=2, max_digits=5)),
                ("quantity", models.PositiveIntegerField(default=1)),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="data_producer.order",
                    ),
                ),
            ],
        ),
    ]
