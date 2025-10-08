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
        "task": "core.apps.havasbook.signals.tasks.send_cart_reminders_task",
        "schedule": crontab(hour=18, minute=0),  # 18:00 ga o'zgartirildi
    },
}
