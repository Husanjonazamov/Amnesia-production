import telebot
from telebot import types
from telebot.types import InputMediaPhoto
from core.apps.havasbook.models import BookModel
from core.apps.havasbook.serializers.order.generate_link import send_payment_options
from config.env import env
from .delivery_date import get_delivery_date


BOT_TOKEN = env("BOT_TOKEN")
CHANNEL_ID = env("CHANNEL_ID")

bot = telebot.TeleBot(token=BOT_TOKEN)




def send_order_to_telegram(order):
    chat_id = CHANNEL_ID

    caption = (
        f"📦 <b>Новый заказ</b> #{order.id}\n\n"
        f"👤 <b>Клиент:</b> {order.reciever_name}\n"
        f"📞 <b>Телефон:</b> {order.reciever_phone}\n"
        f"💰 <b>Общая сумма:</b> {int(order.total_price):,} сум\n"
        f"🗒️ <b>Комментарий:</b> {order.comment or 'Нет'}\n"
        f"💳 <b>Тип оплаты:</b> {order.payment_method.capitalize()}\n\n"
        f"📚 <b>Список товаров:</b>\n"
    )

    image_paths = []
    order_items = order.order_item.all()

    for idx, item in enumerate(order_items, 1):
        book = item.book
        caption += (
            f"\n<b>{idx}. {book.name}</b>\n"
            f"   🔖 <b>ID товара:</b> {book.book_id}\n"
            f"   💵 <b>Цена:</b> {int(item.price):,} сум\n"
            f"   📦 <b>Количество:</b> {item.quantity} шт.\n"
        )
        if book.image and book.image.path:
            image_paths.append(book.image.path)

    if len(image_paths) == 1:
        with open(image_paths[0], 'rb') as img:
            bot.send_photo( 
                chat_id=chat_id,
                photo=img,
                caption=caption,
                parse_mode="HTML",
            )
    elif len(image_paths) > 1:
        media_group = []
        for i, path in enumerate(image_paths):
            with open(path, 'rb') as img:
                media = InputMediaPhoto(img.read())
                if i == 0:
                    media.caption = caption
                    media.parse_mode = "HTML"
                media_group.append(media)

        bot.send_media_group(chat_id=chat_id, media=media_group)




def send_user_order(order):
    user_id = order.user.user_id
    
    message = "📦 Ваш заказ принят. 😊"
    bot.send_message(
        chat_id=user_id,
        text=message
    )
    
    
    
def send_payment_success(order):
    order_id = order.id
    user_id = order.user.user_id
    total_price = order.total_price    
    
    message = (
        f"✅ <b>Оплата прошла успешно!</b>\n\n"
        f"🧾 <b>ID заказа:</b> #{order_id}\n"
        f"👤 <b>Покупатель:</b> {user_id}\n"
        f"💰 <b>Оплачено:</b> {total_price} сум\n\n"
        f"📦 Заказ успешно оформлен и подтвержден. "
        f"Пожалуйста, начните процесс доставки.\n\n"
        f"🕒 <i>Спасибо за покупку!</i>"
    )
    
    
    bot.send_message(
        chat_id=CHANNEL_ID,
        text=message,
        parse_mode="HTML"
    )

