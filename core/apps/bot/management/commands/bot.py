# import telebot
# from telebot import types
# from django.core.management.base import BaseCommand
# from .loader import bot
# from config.env import env
# from core.apps.bot.management.commands.handler import *

# ADMIN_ID = env.int('ADMIN_ID')

# class Command(BaseCommand):
#     help = "Botni ishga tushirish"

#     def add_arguments(self, parser):
#         parser.add_argument('--noinput', action='store_true', help='No input mode for bot')

#     def handle(self, *args, **options):
#         noinput = options['noinput']

#         if noinput:
#             self.stdout.write("Bot ishga tushyapti (noinput rejimida)...")
#         else:
#             self.stdout.write("Bot oddiy rejimda ishga tushyapti...")

#         bot.send_message(ADMIN_ID, text="bot ishga tushdi")
#         self.stdout.write("bot ishga tushirildi")
#         bot.polling()
