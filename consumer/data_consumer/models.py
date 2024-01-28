from django.db import models
from django_celery_results.models import TaskResult
from rest_framework_api_key.models import AbstractAPIKey

# Create your models here.


class TaskAPIKey(AbstractAPIKey):
    task = models.ForeignKey(
        TaskResult,
        on_delete=models.CASCADE,
        related_name="api_keys",
    )
