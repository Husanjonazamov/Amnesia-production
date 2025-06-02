from core.apps.bot.management.commands.loader import bot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from payme import Payme
from config.env import env
from rest_framework.response import Response




PAYME_ID = env.str("PAYME_ID")
PAYME_KEY = env.str("PAYME_KEY")


payme = Payme(
    payme_id=PAYME_ID,
    payme_key=PAYME_KEY
)


def send_payment_link(order):
    user_id = order.user.user_id

    payment_type = order.payment_method
    order_id = order.id
    amount = order.total_price 
         
    if payment_type == "payme":
        pay_link = payme.initializer.generate_pay_link(
            id=int(order_id),  
            amount=amount,
            return_url="https://t.me/Havas_book_bot"
        )
    elif payment_type == "click":
        pay_link = payme.initializer.generate_pay_link(
            id=1,  
            amount=1000,
            return_url="https://t.me/Havas_book_bot"
        )
    elif payment_type == "paynet":
        return Response({
            "detail": "Bu Paynet https://paynet.uz/"
        })
    else:
        return Response({
            "detail": "Bu Uzum card https://uzum.uz/"
        })
       
    markup = InlineKeyboardMarkup()
    button2 = InlineKeyboardButton("💳 To'lov qilish", url=pay_link)
    markup.add(button2)
    
    message_text = (
        "🛒 Hurmatli mijoz!\n\n"
        "Sizning buyurtmangiz uchun to‘lovni amalga oshirish uchun quyidagi tugmani bosing.\n\n"
        "💡 To‘lovni tez va oson amalga oshiring.\n\n"
        "Rahmat! 😊"
    )
    
    
    bot.send_message(
        chat_id=user_id,
        text=message_text,
        reply_markup=markup
    )
