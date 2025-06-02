from datetime import datetime, timedelta, time
from django.utils import timezone
from core.apps.havasbook.models.order import OrderModel


def get_delivery_date():
    now = timezone.localtime()
    today = now.date()

    start_of_day = datetime.combine(today, time(1, 0)).astimezone()
    end_of_day = datetime.combine(today + timedelta(days=1), time(0, 0)).astimezone()
    
    today_orders_count = OrderModel.objects.filter(created_at__range=(start_of_day, end_of_day)).count()

    if today_orders_count > 50:
        delivery_date = today + timedelta(days=2)
    else:
        if now.time() < time(12, 0):
            delivery_date = today + timedelta(days=1)
        else:
            delivery_date = today + timedelta(days=2)

    return delivery_date
