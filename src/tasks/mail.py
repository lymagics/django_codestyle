from django.conf import settings
from django.core.mail import send_mail
from django.template import loader

from celery import shared_task


@shared_task
def mail_send_task(subject: str, email: str, template: str, **context):
    message = loader.render_to_string(template, context)
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
    )
