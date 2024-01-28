import requests
from django.conf import settings
import json


def get_upper_first_three_letters(string):
    if len(string) >= 3:
        return string[:3].upper()
    else:
        return string.ljust(3, "0").upper()


def send_request(order):
    url2 = settings.CONSUMER_DOMAIN + "/api/v1/consumer/process-message/"

    message = build_request_payload(settings.PROVIDER_DOMAIN, order.__dict__)
    headers = {
        "content-type": "application/json",
    }
    json_message = json.dumps(message)
    url1 = "http://192.168.1.8:8000/api/v1/consumer/send-message/"
    # response = requests.post(url=url, data=json_message,headers=headers)
    response = requests.post(url=url1, data=json_message, headers=headers)
    response = requests.post(url=url2, data=json_message, headers=headers)
    return response


def build_request_payload(api_url, order):
    webhook_url = (
        api_url + "/api/v1/data/orders/" + str(order.get("uuid")) + "/status/update"
    )
    return {
        "webhook_url": webhook_url,
        "address": order.get("address"),
        "phone_number": str(order.get("phone_number")),
        "order_key": order.get("order_key"),
        "status": order.get("status"),
        "currency": order.get("currency"),
    }
