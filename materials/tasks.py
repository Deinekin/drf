from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from materials.models import Course, Subscription


@shared_task
def send_course_change(pk):
    """Send information when course is changed."""
    course = Course.objects.get(pk=pk)
    subscriptions_list = Subscription.objects.filter(course=pk)
    email_list = []
    if subscriptions_list:
        email_list = [subs.user.email for subs in subscriptions_list]
    if email_list:
        send_mail(
            subject="Обновление курса",
            message="Ваш курс был обновлен",
            from_email=EMAIL_HOST_USER,
            recipient_list=[email_list],
        )
