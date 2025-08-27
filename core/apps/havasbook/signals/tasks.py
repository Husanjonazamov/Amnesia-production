from celery import shared_task
from core.apps.havasbook.models import CartModel
from config.env import env
import requests


BOT_TOKEN = env("BOT_TOKEN")


def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": chat_id, "text": text})
    except Exception as e:
        print(f"Xabar yuborishda xato: {e}")
        

@shared_task
def send_cart_reminder_task(cart_id):
    try:
        cart = CartModel.objects.get(id=cart_id)
        chat_id = cart.user.tg_id
        product_name = cart.product.name
        send_message(
            chat_id, 
            f"Здравствуйте! 🛒 Товар «{product_name}» всё ещё ждёт вас в вашей корзине. Не пропустите возможность оформить заказ!"
        )

    except CartModel.DoesNotExist:
        pass
