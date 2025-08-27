from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from core.apps.havasbook.models import CartModel


class CartNotificationAPIView(APIView):
    def get(self, request):
        carts = CartModel.objects.filter(cart_items__isnull=False).distinct()

        if not carts.exists():
            return Response(
                {"message": "Hech bir foydalanuvchining savati to‘ldirilmagan"},
                status=status.HTTP_404_NOT_FOUND
            )

        notifications = []
        for cart in carts:
            items = cart.cart_items.all()
            total_amount = sum([float(item.total_price) for item in items])

            notifications.append({
                "tg_id": cart.user.user_id,
                "products": [
                    {
                        "book": item.book.name,
                        "quantity": item.quantity,
                        "total_price": float(item.total_price)
                    } for item in items
                ],
                "total_amount": total_amount
            })

        return Response(
            {
                "count": len(notifications),
                "notifications": notifications
            },
            status=status.HTTP_200_OK
        )
