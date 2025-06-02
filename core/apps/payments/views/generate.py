# from rest_framework import status, views
# from rest_framework.response import Response
# from django.shortcuts import get_object_or_404
# from core.apps.havasbook.models.order import OrderModel
# from core.apps.accounts.models.user import User

# from rest_framework.permissions  import AllowAny
# from core.apps.user.permissions.user import UserPermission
# from payme import Payme
# from config.env import env
# from core.apps.bot.management.commands.handler.generate import send_payment_link

# PAYME_ID = env.str("PAYME_ID")
# PAYME_KEY = env.str("PAYME_KEY")

# print("------", PAYME_KEY, PAYME_ID, "---")

# payme = Payme(
#     payme_id=PAYME_ID,
#     payme_key=PAYME_KEY
# )

# class OrderPaymentLinkView(views.APIView):
#     permission_classes = [AllowAny, UserPermission]
    
#     def post(self, request):
#         order_id = request.data.get("order_id")

#         if not order_id:
#             return Response({"error": "order_id is required"}, status=400)

#         order = get_object_or_404(OrderModel, id=order_id)
#         payment_type = order.payment_method

#         if not order.user:  
#             return Response({"error": "Orderga bog'liq foydalanuvchi topilmadi"}, status=400)

#         amount = order.total_price 
         
#         if payment_type == "payme":
#             pay_link = payme.initializer.generate_pay_link(
#                 id=int(order_id),  
#                 amount=amount,
#                 return_url=""
#             )
#         elif payment_type == "click":
#             return Response({
#                 "detail": "Bu Click https://click.uz/"
#             })
#         elif payment_type == "paynet":
#             return Response({
#                 "detail": "Bu Paynet https://paynet.uz/"
#             })
#         else:
#             return Response({
#                 "detail": "Bu Uzum card https://uzum.uz/"
#             })
        
        
#         send_payment_link(order, pay_link)
        
#         result = {
#             "order_id": order.id,
#             "user_id": order.user.user_id,
#             "total_price": order.total_price * 100,   
#             "pay_link": pay_link
#         }

#         return Response(result, status=200)
