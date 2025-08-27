from django.db.models.signals import post_save
from django.dispatch import receiver
import requests

from core.apps.havasbook.models import CartModel
from config.env import env

BOT_TOKEN = env("BOT_TOKEN")


def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": chat_id, "text": text})
    except Exception as e:
        print(f"Xabar yuborishda xato: {e}")



@receiver(post_save, sender=CartModel)
def CartSignal(sender, instance, created, **kwargs):
    if created:
        try:
            from core.apps.havasbook.signals.tasks import send_cart_reminder_task
            send_cart_reminder_task.apply_async(
                args=[instance.id],
                countdown=5 
            )
        except ImportError:
            send_message(instance.user.tg_id, f"{instance.product.name} sizning savatchangizda kutyapti!")
