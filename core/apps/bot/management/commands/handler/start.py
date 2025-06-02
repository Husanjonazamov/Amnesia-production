from telebot import types
from ..loader import bot
from ..utils import get_inline_keyboard
from ..utils import texts
from telebot.types import MenuButtonWebApp, WebAppInfo
from config.env import env


web_app_info = WebAppInfo(url=env("WEB_APP_URL"))
menu_button = MenuButtonWebApp(
    type="web_app",
    text="📦 Magazin",
    web_app=web_app_info
)


@bot.message_handler(commands=['start'])
def start(message):
    bot.set_chat_menu_button(chat_id=message.chat.id, menu_button=menu_button)
    bot.send_message(message.chat.id, text=texts.START.format(message.from_user.first_name), reply_markup=get_inline_keyboard())