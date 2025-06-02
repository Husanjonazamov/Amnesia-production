from payme.views import PaymeWebHookAPIView
from core.apps.havasbook.serializers.order.send_order import send_user_order, send_payment_success
from core.apps.havasbook.models import OrderModel


class PaymeCallBackAPIView(PaymeWebHookAPIView):
    def handle_created_payment(self, params, result, *args, **kwargs):
        """
        Handle the successful payment. You can override this method
        """
        print(f"Transaction created for this params: {params} and cr_result: {result}")


    def handle_successfully_payment(self, params, result, *args, **kwargs):
        """
        Handle the successful payment. You can override this method
        """
        try:
            order_id = int(params.get("account", {}).get("id"))
            order = OrderModel.objects.get(id=order_id)
            print(order_id)
            send_user_order(order)
            send_payment_success(order)
        except OrderModel.DoesNotExist:
            print(f"Order with ID {order_id} not found.")            

        print(f"Transaction successfully performed for this params: {params} and performed_result: {result}")

    def handle_cancelled_payment(self, params, result, *args, **kwargs):
        """
        Handle the cancelled payment. You can override this method
        """
        print(f"Transaction cancelled for this params: {params} and cancelled_result: {result}")
        



