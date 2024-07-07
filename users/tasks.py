from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def check_user_last_login():
    """Makes user inactive if he hasn't visited site for a month"""

    users = User.objects.filter(is_active=True)
    for user in users:
        if user.last_login:
            if timezone.now() - user.last_login > timedelta(days=30):
                user.is_active = False
                user.save()
