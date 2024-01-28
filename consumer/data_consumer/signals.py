from django.dispatch import receiver
from django.db.models.signals import post_save
from .tasks import notify_producer
from django_celery_results.models import TaskResult
import logging

logger = logging.getLogger(__name__)


def celery_task_notify(created, task):
    if created:
        task = {"task_id": str(task.task_id), "result": str(task.result)}

        notify_producer.delay(task)


@receiver(post_save, sender=TaskResult)
def signal_handler_post_save_TaskResult(sender, instance, created, **kwargs):
    celery_task_notify(created=created, task=instance)
