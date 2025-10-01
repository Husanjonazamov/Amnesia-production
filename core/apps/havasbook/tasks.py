# from celery import shared_task
# import requests
# import logging
# from config.env import env

# TELEGRAM_BOT_TOKEN = env.str("BOT_TOKEN")
# TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

# logger = logging.getLogger(__name__)



# @shared_task
# def send_cart_reminders():
#     from core.apps.cart.models import CartModel
    
#     logger.info("=== Celery task send_cart_reminders ishga tushdi ===")
    
#     carts = CartModel.objects.prefetch_related('cart_items__book').all()
    
#     for cart in carts:
#         user = cart.user
#         tg_id = user.user_id
#         items = cart.cart_items.all()
        
#         if not items.exists():
#             logger.info(f"Foydalanuvchi {user.first_name} savati bo'sh, o'tkazildi")
#             continue
        
#         product_lines = "\n".join([f"• {item.book.name} x {item.quantity}" for item in items])
#         message_text = (
#             f"🛒 Ваши товары ждут вас в корзине!\n\n"
#             f"{product_lines}\n\n"
#             "Не упустите возможность оформить заказ! 😉"
#         )
        
#         try:
#             response = requests.get(TELEGRAM_API_URL, params={"chat_id": tg_id, "text": message_text})
#             if response.status_code == 200:
#                 logger.info(f"Foydalanuvchi {user.first_name} (TG ID: {tg_id}) ga habar yuborildi")
#             else:
#                 logger.warning(f"Habar yuborilmadi {user.first_name} (TG ID: {tg_id}), status_code: {response.status_code}")
#         except Exception as e:
#             logger.error(f"Habar yuborishda xato {user.first_name} (TG ID: {tg_id}): {str(e)}")
    
#     logger.info("=== Celery task send_cart_reminders tugadi ===")
