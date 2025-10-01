from celery import shared_task
import requests
import logging
from config.env import env

from core.apps.havasbook.models import CartModel

TELEGRAM_BOT_TOKEN = env.str("BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

logger = logging.getLogger(__name__)




@shared_task
def send_cart_reminders():
    carts = CartModel.objects.prefetch_related('cart_items__book').all()
    for cart in carts:
        user = cart.user
        tg_id = user.user_id
        items = cart.cart_items.all()
        
        if not items.exists():
            continue
        
        product_lines = "\n".join([f"• {item.book.name} x {item.quantity}" for item in items])
        message_text = (
            f"🛒 Ваши товары ждут вас в корзине!\n\n"
            f"{product_lines}\n\n"
            "Не упустите возможность оформить заказ! 😉"
        )
        
        try:
            response = requests.get(TELEGRAM_API_URL, params={"chat_id": tg_id, "text": message_text})
        except Exception as e:
            logger.error(f"Habar yuborishda xato {user.first_name} (TG ID: {tg_id}): {str(e)}")
    
