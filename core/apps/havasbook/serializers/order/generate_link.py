from telebot import types

def send_payment_options(order, bot):
    markup = types.InlineKeyboardMarkup()

    # Buyurtma ko'rish tugmasi
    order_url = f"http://127.0.0.1:8081/order/{order.id}"
    markup.add(types.InlineKeyboardButton("Buyurtmani ko‘rish", url=order_url))

    if order.payment_method == "click":
        payment_url = f"https://click.uz/pay/{order.user.user_id}?amount={order.total_price}"
        markup.add(types.InlineKeyboardButton("Click orqali to'lov", url=payment_url))
        bot.send_message(
            chat_id=order.user.user_id,
            text=f"Sizning buyurtmangiz {order.id} qabul qilindi. Tez orada siz bilan bog`lanamiz.\n",
            reply_markup=markup
        )
    
    elif order.payment_method == "payme":
        payment_url = f"https://payme.uz/pay/{order.user.user_id}?amount={order.total_price}"
        markup.add(types.InlineKeyboardButton("Payme orqali to'lov", url=payment_url))
        bot.send_message(
            chat_id=order.user.user_id,
            text=f"Sizning buyurtmangiz {order.id} qabul qilindi. Tez orada siz bilan bog`lanamiz.\n",
            reply_markup=markup
        )

    elif order.payment_method == "paynet":
        payment_url = f"https://paynet.uz/pay/{order.user.user_id}?amount={order.total_price}"
        markup.add(types.InlineKeyboardButton("Paynet orqali to'lov", url=payment_url))
        bot.send_message(
            chat_id=order.user.user_id,
            text=f"Sizning buyurtmangiz {order.id} qabul qilindi. Tez orada siz bilan bog`lanamiz.\n",
            reply_markup=markup
        )

    else:
        # Uzum to'lov tizimi
        payment_url = f"https://uzum.uz/pay/{order.user.user_id}?amount={order.total_price}"
        markup.add(types.InlineKeyboardButton("Uzum orqali to'lov", url=payment_url))
        bot.send_message(
            chat_id=order.user.user_id,
            text=f"Sizning buyurtmangiz {order.id} qabul qilindi. Tez orada siz bilan bog`lanamiz.\n",
            reply_markup=markup
        )
