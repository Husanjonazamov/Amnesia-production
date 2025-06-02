from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel
from core.apps.accounts.models import User




class Status(models.TextChoices):
    NEW = 'new', _('Yangi')
    ACCEPTED = 'accepted', _('Qabul qilindi')
    CANCELLED = 'cancelled', _('Bekor qilindi')


class PaymentMethodChoice(models.TextChoices):
    CASH = "cash", _("Naqt pul")
    CLICK = "click", _("Click")
    PAYME = "payme", _("Payme")
    PAYNET = "paynet", _("Paynet")
    UZUM = "uzum_card", _("Uzum karta")


 
class OrderStatus(models.TextChoices):
    NEW = "new", _("Yangi")
    DELIVERED = "delivered", _("Topshirilgan")
    CANCELLED = "cancelled", _("Bekor qilingan")



class PreorderModel(AbstractBaseModel):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name="preorder"
    )
    book = models.ForeignKey(
        'havasbook.BookModel',
        on_delete=models.CASCADE,
        related_name="book"
    )
    count = models.PositiveIntegerField(
        _("Mahlulot Soni"),
        default=1
    )
    reciever_name = models.CharField(
        _("Foydalanuvchi ismi"),
        max_length=250, 
        null=True,
        blank=True
    )
    payment_method = models.CharField(
        _("To'lov turi"),
        max_length=50,
        choices=PaymentMethodChoice.choices,
        default='click'
    )
    status = models.CharField(
        _("Status"),
        max_length=50,
        choices=OrderStatus.choices,
        default=OrderStatus.NEW
    )  

    location = models.ForeignKey(
        "havasbook.LocationModel",
        on_delete=models.CASCADE,
        related_name="preorder",
    )
    delivery_method = models.ForeignKey(
        'havasbook.DeliveryModel',
        on_delete=models.CASCADE,
        related_name="preorder",
        null=True, blank=True
    )
    reciever_phone = models.CharField(
        _("Telefon raqam"),
        max_length=100,
        null=True,
        blank=True
    )

    color = models.ForeignKey('havasbook.ColorModel', on_delete=models.SET_NULL, null=True, blank=True)
    size = models.ForeignKey('havasbook.SizeModel', on_delete=models.SET_NULL, null=True, blank=True)

    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 



    def __str__(self):
        return self.book.name



    @classmethod
    def _create_fake(self):
        return self.objects.create(
            name="Test",
        )

    class Meta:
        db_table = "preorder"
        verbose_name = _("PreorderModel")
        verbose_name_plural = _("PreorderModels")
