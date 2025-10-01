"""
Celery configurations
"""

import os
import celery
from celery.schedules import crontab 
from config.env import env

os.environ.setdefault("DJANGO_SETTINGS_MODULE", env("DJANGO_SETTINGS_MODULE"))

app = celery.Celery("config")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


app.conf.beat_schedule = {
    "send-cart-reminders-everyday": {
        "task": "core.apps.havasbook.signals.tasks.send_cart_reminders",
        "schedule": crontab(hour=12, minute=00), 
        "args": (12, 00), 
    },
}
