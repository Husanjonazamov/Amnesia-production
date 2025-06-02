import telebot
from core.apps.havasbook.models import OrderModel

bot = telebot.TeleBot("7178118588:AAHtJ8mKY-ChU0yyxiyWhcVogURQwki61_Y")

def send_cancel_order(order):
    chat_id = "-1002264446732" 

    cancel_message = f"🚫 #{order.id} sonli buyurtma bekor qilindi.\n" \
                     f"👤 Foydalanuvchi: {order.user.first_name if order.user else 'Noma\'lum'}\n" \
                     f"📞 Tel: {order.phone or 'Ko\'rsatilmagan'}\n" \
                     f"💬 Izoh: {order.comment or 'Yo\'q'}"

    try:
        bot.send_message(chat_id=chat_id, text=cancel_message)
    except Exception as e:
        print(f"[Telegram Error] Xabar yuborilmadi: {e}")
