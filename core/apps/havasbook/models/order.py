from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel



class DeliveryMethodChoice(models.TextChoices):
    DOOR_DELIVERY = "door_delivery", _("Eski uyga (Toshkent bo'ylab kur'er orqali yetkazib berish) 20.000~35.000 so'm")
    PICKUP_POINT = "pickup_point", _("Yetkazib berish nuqtasiga (BTS pochta orqali O'zbekiston bo'ylab) 25.000~50.000 so'm")


class PaymentMethodChoice(models.TextChoices):
    CLICK = "click", _("Click")
    PAYME = "payme", _("Payme")
    PAYNET = "paynet", _("Paynet")
    UZUM = "uzum_card", _("Uzum karta")


 
class OrderStatus(models.TextChoices):
    NEW = "new", _("Yangi")
    DELIVERED = "delivered", _("Topshirilgan")
    CANCELLED = "cancelled", _("Bekor qilingan")


class OrderType(models.TextChoices):
    ORDER = "order", _("Oddiy buyurtma")
    PREORDER = "preorder", _("Oldindan buyurtma")



class OrderModel(AbstractBaseModel):
    user = models.ForeignKey(
        "accounts.User", 
        on_delete=models.CASCADE,
        related_name="orders"
    )
    reciever_name = models.CharField(_("Ism"), max_length=100,  null=True, blank=True)
    reciever_phone = models.CharField(_("Telefon raqam"), max_length=100, null=True, blank=True)
    location = models.ForeignKey(
        "havasbook.LocationModel",
        on_delete=models.CASCADE,
        related_name="orders",
    )
    delivery_method = models.ForeignKey(
        'havasbook.DeliveryModel',
        on_delete=models.CASCADE,
        related_name="orders",
        null=True, blank=True
    )
    order_type = models.CharField(
        verbose_name=_("Buyurtma turi"),
        max_length=100,
        choices=OrderType.choices,
        default=OrderType.ORDER
    )
     
    payment_method = models.CharField(
        _("To'lov turi"),
        max_length=50,
        choices=PaymentMethodChoice.choices,
        default='click'
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 
    status = models.CharField(
        _("Status"),
        max_length=50,
        choices=OrderStatus.choices,
        default=OrderStatus.NEW
    )  
    comment = models.TextField(_("Buyrtma uchun izoh"), null=True, blank=True) 


    def __str__(self):
        return self.user.first_name


    @classmethod
    def _create_fake(self):
        return self.objects.create(
            name="Test",
        )

    class Meta:
        db_table = "order"
        verbose_name = _("OrderModel")
        verbose_name_plural = _("OrderModels")


class OrderitemModel(AbstractBaseModel):
    order = models.ForeignKey(
        OrderModel, 
        on_delete=models.CASCADE,
        related_name="order_item",
    )
    book = models.ForeignKey(
        "havasbook.BookModel",
        on_delete=models.CASCADE,
        related_name="order_item"
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  


    def __str__(self):
        return self.order.reciever_name

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            name="Test",
        )

    class Meta:
        db_table = "orderITem"
        verbose_name = _("OrderitemModel")
        verbose_name_plural = _("OrderitemModels")
