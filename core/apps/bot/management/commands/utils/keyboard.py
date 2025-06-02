from telebot.types import (
    ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
)
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from config.env import env


CONTACT = "📞 Bog'lanish"


WEB_APP_URL = env("WEB_APP_URL")


def get_inline_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)

    shop = InlineKeyboardButton(
        text="🛍 Magazin",
        web_app=WebAppInfo(url=WEB_APP_URL)
    )
    ordering = InlineKeyboardButton(
        text="📦 Buyurtmalarim",
        web_app=WebAppInfo(url=WEB_APP_URL)
    )
    sale = InlineKeyboardButton(
        text="🔥 Aksiyalar",
        web_app=WebAppInfo(url=WEB_APP_URL)
    )
    contact = InlineKeyboardButton(
        text=CONTACT,
        callback_data="contact"
    )

    keyboard.add(shop)
    keyboard.add(sale, ordering)
    keyboard.add(contact)

    return keyboard
