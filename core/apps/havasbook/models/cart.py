from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel
from core.apps.accounts.models.user import User
from django.db.models import Sum


class CartModel(AbstractBaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="carts"
    )
    total_price = models.DecimalField(
        max_digits=30,
        decimal_places=2,
        default=0.00
    )
    
    def __str__(self):
        return self.user.first_name
        
    @classmethod
    def _create_fake(self):
        return self.objects.create(
            name="Test",
        )

    class Meta:
        db_table = "cart"
        verbose_name = _("Корзина")
        verbose_name_plural = _("Корзины")



class CartitemModel(AbstractBaseModel):
    cart = models.ForeignKey(
        CartModel,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )
    book = models.ForeignKey(
        'havasbook.BookModel',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveBigIntegerField(_("Количество товара"), default=1)
    color = models.ForeignKey(
        'havasbook.ColorModel',
        on_delete=models.CASCADE,
        null=True, 
        blank=True
    )
    size = models.ForeignKey(
        'havasbook.SizeModel',
        on_delete=models.CASCADE,
        null=True, 
        blank=True
    )
    total_price = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0.00
    )
    
    def __str__(self):
        return self.book.name

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            name="Test",
        )

    class Meta:
        db_table = "cartItem"
        verbose_name = _("Товар в корзине")
        verbose_name_plural = _("Товары в корзине")
