from celery import shared_task
import requests
from django.conf import settings

@shared_task
def send_push_notification(title, message):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    payload = {
        'to': '<EXPO_PUSH_TOKEN>',
        'sound': 'default',
        'title': title,
        'body': message,
    }
    response = requests.post(settings.EXPO_PUSH_NOTIFICATION_URL, json=payload, headers=headers)
    return response.status_code
