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




def send_order_to_telegram(order, location_name, latitude, longitude):
    chat_id = CHANNEL_ID
    yandex_url = f"https://yandex.com/maps/?pt={longitude},{latitude}&z=14&l=map"

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📍 Manzilni ko‘rish", url=yandex_url))

    caption = (
        f"📦 <b>Yangi Buyurtma</b> #{order.id}\n\n"
        f"👤 <b>Buyurtmachi:</b> {order.reciever_name}\n"
        f"📞 <b>Telefon:</b> {order.reciever_phone}\n"
        f"📍 <b>Joylashuv:</b> {location_name}\n"
        f"💰 <b>Jami summa:</b> {int(order.total_price):,} so'm\n"
        f"🗒️ <b>Izoh:</b> {order.comment or 'Yo‘q'}\n"
        f"💳 <b>To'lov turi:</b> {order.payment_method.capitalize()}\n\n"
        f"📚 <b>Buyurtmadagi kitoblar:</b>\n"
    )

    image_paths = []
    order_items = order.order_item.all()

    for idx, item in enumerate(order_items, 1):
        book = item.book
        caption += (
            f"\n<b>{idx}. {book.name}</b>\n"
            f"   🔖 <b>Kitob ID:</b> {book.book_id}\n"
            f"   💵 <b>Narxi:</b> {int(item.price):,} so'm\n"
            f"   📦 <b>Miqdori:</b> {item.quantity} dona\n"
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
                reply_markup=markup
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
        bot.send_message(chat_id=chat_id, text="📍 <b>Manzilni ko‘rish uchun tugmani bosing:</b>", parse_mode="HTML", reply_markup=markup)
    else:
        bot.send_message(chat_id=chat_id, text=caption, parse_mode="HTML", reply_markup=markup)




def send_user_order(order):
    user_id = order.user.user_id
    
    delivery_date = get_delivery_date()
    message = f"📦 Buyurtmangiz {delivery_date.strftime('%Y-yil %B oyining %d-kuni')} yetkazib beriladi. 😊"    
    bot.send_message(
        chat_id=user_id,
        text=message
    )
    
    
    
def send_payment_success(order):
    order_id = order.id
    user_id = order.user.user_id
    total_price = order.total_price    
    
    message = (
        f"✅ <b>To‘lov muvaffaqiyatli amalga oshirildi!</b>\n\n"
        f"🧾 <b>Buyurtma ID:</b> #{order_id}\n"
        f"👤 <b>Mijoz:</b> {user_id}\n"
        f"💰 <b>To‘langan summa:</b> {total_price} so'm\n\n"
        f"📦 Buyurtma to‘liq rasmiylashtirildi va tasdiqlandi. "
        f"Iltimos, yetkazib berish jarayonini boshlang.\n\n"
        f"🕒 <i>Rahmat sizga!</i>"
    )
    
    
    bot.send_message(
        chat_id=CHANNEL_ID,
        text=message,
        parse_mode="HTML"
    )

