from django.db.models.signals import post_save
from django.dispatch import receiver
from utils.email import send_email_notif_to_admin
from .models import ContactUs


@receiver(post_save, sender=ContactUs)
def send_contact_notification_email(sender, instance, created, **kwargs):
    if created:
        subject = 'یک پیام جدید ثبت شده است'
        message = f'{instance.user}: {instance.message}'
        send_email_notif_to_admin.apply_async(
            (subject, message),
            retry=False,
            ignore_result=True,
            expires=180,
        )
