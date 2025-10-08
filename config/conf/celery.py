from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    "send-cart-reminders-every-day": {
        "task": "core.apps.cart.tasks.send_cart_reminders_task",
        "schedule": crontab(hour=18, minute=0), 
    },
}
