from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


def create_dev_user(*args, **kwargs):
    if settings.DEBUG:
        payload = {
            "email": "shevado@ukr.net",
            "username": "nedtyb",
            "password": "nedtyb",
            "first_name": "Admin",
            "last_name": "Adminovich",
            "age": 36,
            "phone": "0951111111",
        }

        User.objects.create_superuser(**payload)
