from celery import shared_task
from django.conf import settings
from django_celery_results.models import TaskResult
import requests
from .utils import send
import uuid
import json

# question 7
@shared_task
def change_status_data(message_data, webhook_url):
    message_data["status"] = "confirmed"
    task_result = TaskResult.objects.create(
        task_id=change_status_data.request.id, result=message_data
    )
    task_id = task_result.task_id

    send(message_data["status"], webhook_url, task_id)


# question 6
@shared_task
def process_data(status, currency, order_key):
    result_value = status + currency + order_key
    task_id = str(uuid.uuid4())
    task_result = TaskResult.objects.create(task_id=task_id, result=result_value)
    print(TaskResult.objects.all())


def _notify(task):
    domain = settings.PROVIDER_DOMAIN
    url = domain + "/api/v1/data/task-results/"

    headers = {
        "content-type": "application/json",
        "X-Api-Key": settings.PRODUCER_API_KEY,
    }

    json_message = json.dumps(task)

    response = requests.post(url, data=json_message, headers=headers)

    if response.status_code == 200:
        print("Request to API successful!")
    else:
        print(f"Request to API failed. Status code: {response.status_code}")


@shared_task()
def notify_producer(task):
    _notify(task)


# producer call celery task information and consumer will give him the information about the task

# producer will get the celery task result from the consumer

# celery task is saved a signal will send the result to the producer

# make tests and run them

# try to change to rubbitmq
