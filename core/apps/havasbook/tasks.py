import requests
from celery import shared_task
from config.env import env
from django.contrib.auth import get_user_model
from core.apps.havasbook.models.cart import CartModel

BOT_TOKEN = env.str("BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"




@shared_task
def send_cart_reminder(user_id):
    try:
        User = get_user_model()
        user = User.objects.get(id=user_id)
        tg_id = user.user_id 

        cart = CartModel.objects.prefetch_related('cart_items__book').filter(user=user).first()
        if not cart:
            return

        items = cart.cart_items.all()
        if not items.exists():
            return

        product_lines = "\n".join([f"• {item.book.name} x {item.quantity}" for item in items])
        message_text = (
            f"🛒 Ваши товары ждут вас в корзине!\n\n"
            f"{product_lines}\n\n"
            "Не упустите возможность оформить заказ! 😉"
        )

        response = requests.get(TELEGRAM_API_URL, params={"chat_id": tg_id, "text": message_text})
        if response.status_code == 200:
                print(f"✅ Telegram eslatma yuborildi: {user.username} (tg_id: {tg_id})")
        else:
            print(f"❌ Telegram xato ({response.status_code}): {user.username} (tg_id: {tg_id}) - {response.status_code}")


    except Exception as e:
        print(f"Xatolik: {e}")


@shared_task(name="core.apps.havasbook.tasks.send_cart_reminders_task")
def send_cart_reminders_task():
    carts = CartModel.objects.prefetch_related('cart_items__book').all()
    sent_count = 0 

    for cart in carts:
        if cart.cart_items.exists():
            send_cart_reminder.delay(cart.user.id)
            sent_count += 1

    print(f"📊 Eslatmalar yuborildi: {sent_count} ta userga")
