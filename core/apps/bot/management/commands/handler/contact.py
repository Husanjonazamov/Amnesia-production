from telebot import types
from ..loader import bot
from ..utils import texts, keyboard





@bot.message_handler(func=lambda message: message.text.startswith(keyboard.CONTACT))
def contact(message: types.Message):
    
    print('----')
    """
    Bot boʻyicha toʻliq maʼlumot olish: @Husanboy_Azamov

    ☎️ Bogʻlanish uchun telefon: +998 94 001 47 41
    """
    
    bot.send_message(message.chat.id, texts.CONTACTS)

