import requests
from django.conf import settings
from rest_framework.response import Response
import json


def send(status, webhook_url, task_id):

    message = build_request_payload(status, task_id)

    headers = {
        "content-type": "application/json",
        "X-Api-Key": settings.PRODUCER_API_KEY,
    }
    json_message = json.dumps(message)

    response = requests.post(webhook_url, data=json_message, headers=headers)

    if response.status_code == 200:
        print("Request to API successful!")
    else:
        print(f"Request to API failed. Status code: {response.status_code}")
        return Response(
            {"error": f"Request to API failed. Status code: {response.status_code}"},
            status=response.status_code,
        )


def build_request_payload(status, task_id):
    return {
        "taskId": task_id,
        "status": status,
    }
