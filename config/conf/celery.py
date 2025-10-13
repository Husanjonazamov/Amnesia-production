from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    "send-cart-reminders-every-day": {
        "task": "core.apps.havasbook.tasks.send_cart_reminders_task",
        "schedule": crontab(hour=20, minute=00), 
    },
}
