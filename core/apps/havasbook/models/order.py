from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel


class DeliveryMethodChoice(models.TextChoices):
    DOOR_DELIVERY = "door_delivery", _("На дом (доставка курьером по Ташкенту) 20.000~35.000 сум")
    PICKUP_POINT = "pickup_point", _("В пункт выдачи (через BTS-почту по Узбекистану) 25.000~50.000 сум")



class PaymentMethodChoice(models.TextChoices):
    CLICK = "click", _("Click")
    PAYME = "payme", _("Payme")
    PAYNET = "paynet", _("Paynet")
    UZUM = "uzum_card", _("Карта Uzum")



class OrderStatus(models.TextChoices):
    NEW = "new", _("Новый")
    DELIVERED = "delivered", _("Доставлен")
    CANCELLED = "cancelled", _("Отменен")


class OrderType(models.TextChoices):
    ORDER = "order", _("Обычный заказ")
    PREORDER = "preorder", _("Предзаказ")


class OrderModel(AbstractBaseModel):
    user = models.ForeignKey(
        "accounts.User", 
        on_delete=models.CASCADE,
        related_name="orders"
    )
    reciever_name = models.CharField(_("Имя получателя"), max_length=100, null=True, blank=True)
    reciever_phone = models.CharField(_("Номер телефона"), max_length=100, null=True, blank=True)
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
        verbose_name=_("Тип заказа"),
        max_length=100,
        choices=OrderType.choices,
        default=OrderType.ORDER
    )
    payment_method = models.CharField(
        _("Метод оплаты"),
        max_length=50,
        choices=PaymentMethodChoice.choices,
        default='click'
    )
    total_price = models.DecimalField(_("Общая сумма"), max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(
        _("Статус"),
        max_length=50,
        choices=OrderStatus.choices,
        default=OrderStatus.NEW
    )  
    comment = models.TextField(_("Комментарий к заказу"), null=True, blank=True) 

    def __str__(self):
        return self.user.first_name

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            name="Тест",
        )

    class Meta:
        db_table = "order"
        verbose_name = _("Заказ")
        verbose_name_plural = _("Заказы")


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
    quantity = models.PositiveIntegerField(_("Количество"), default=1)
    price = models.DecimalField(_("Цена"), max_digits=10, decimal_places=2)

    def __str__(self):
        return self.order.reciever_name

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            name="Тест",
        )

    class Meta:
        db_table = "orderItem"
        verbose_name = _("Товар в заказе")
        verbose_name_plural = _("Товары в заказе")
