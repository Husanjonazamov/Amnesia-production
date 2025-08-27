from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.apps.havasbook.models import CartModel



class CartNotificationAPIView(APIView):
    def get(self, request, tg_id):
        cart = CartModel.objects.filter(user__user_id=tg_id).first()

        if not cart:
            return Response(
                {"has_items": False, "message": "Savat topilmadi"},
                status=status.HTTP_404_NOT_FOUND
            )

        items = cart.cart_items.all()
        if not items.exists():
            return Response(
                {"has_items": False, "message": "Savat bo'sh"},
                status=status.HTTP_200_OK
            )

        products = []
        total_amount = 0
        for item in items:
            total_amount += float(item.total_price)
            products.append({
                "book": item.book.name,
                "quantity": item.quantity,
                "total_price": float(item.total_price)
            })

        return Response(
            {
                "has_items": True,
                "products": products,
                "total_amount": total_amount
            },
            status=status.HTTP_200_OK
        )
