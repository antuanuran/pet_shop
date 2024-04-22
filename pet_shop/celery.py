import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pet_shop.settings")

app = Celery("pet_shop")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
