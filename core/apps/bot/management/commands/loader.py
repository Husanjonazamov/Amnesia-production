import telebot
from config.env import env
import logging


BOT_TOKEN = env.str('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

logging.basicConfig(level=logging.INFO)











