# from django.db.models.signals import post_save
# from django.dispatch import receiver
# import requests
# import time

# from core.apps.havasbook.models import CartModel
# from config.env import env

# BOT_TOKEN = env("BOT_TOKEN")


# def send_message(chat_id, text):
#     url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
#     try:
#         response = requests.post(url, data={"chat_id": chat_id, "text": text})
#         if response.status_code == 200:
#             print(f"[INFO] Xabar yuborildi foydalanuvchi {chat_id}")
#         else:
#             print(f"[ERROR] Telegram xabar yuborilmadi, status_code: {response.status_code}")
#     except Exception as e:
#         print(f"[ERROR] Xabar yuborishda xato: {e}")


# @receiver(post_save, sender=CartModel)
# def CartSignal(sender, instance, created, **kwargs):
#     print(f"[INFO] post_save signal ishga tushdi, created={created}")

#     try:
#         items = instance.cart_items.all()
#         print(f"[DEBUG] Savatchadagi elementlar: {items}")

#         if not items.exists():
#             print("[INFO] Savatcha bo'sh, xabar yuborilmadi.")
#             return

#         chat_id = instance.user.user_id

#         text_lines = [f"«{item.book.name}» x {item.quantity}" for item in items]
#         message_text = (
#             "Здравствуйте! 🛒 В вашей корзине:\n"
#             + "\n".join(text_lines)
#             + "\n\nНе пропустите возможность оформить заказ!"
#         )

#         print(f"[INFO] Xabar tayyorlanmoqda foydalanuvchi {chat_id}:\n{message_text}")

#         time.sleep(5)

#         send_message(chat_id, message_text)

#     except Exception as e:
#         print(f"[ERROR] Signal ichida xato: {e}")
