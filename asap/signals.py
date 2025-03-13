from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from .tasks import send_push_notification

@receiver(post_save, sender=Notification)
def send_notification(sender, instance, created, **kwargs):
    if created:
        send_push_notification.delay(instance.title, instance.content)
