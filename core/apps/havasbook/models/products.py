from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel


class ProductsModel(AbstractBaseModel):
    name = models.CharField(_("Название"), max_length=255)
    description = models.TextField(_("Описание продукта"), null=True, blank=True)

    category = models.ForeignKey(
        "havasbook.CategoryModel",
        verbose_name=_("Категория"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )

    image = models.ImageField(_("Изображение"), upload_to="product-image/", null=True, blank=True)

    original_price = models.DecimalField(
        _("Исходная цена"), max_digits=10, decimal_places=2, null=True, blank=True
    )
    price = models.DecimalField(
        _("Цена со скидкой"), max_digits=10, decimal_places=2, null=True, blank=True
    )
    is_discount = models.BooleanField(_("Есть ли скидка?"), default=False)
    discount_percent = models.DecimalField(
        _("Процент скидки"), max_digits=10, decimal_places=2, null=True, blank=True
    )

    quantity = models.PositiveIntegerField(
        _("Количество товара"), default=0, null=True, blank=True
    )

    sold_count = models.PositiveIntegerField(
        _("Количество продаж"),
        default=0
    )

    view_count = models.PositiveIntegerField(
        _("Количество просмотров"),
        default=0
    )

    is_preorder = models.BooleanField(
        _("Доступен предзаказ?"),
        default=False
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.discount_percent is not None:
            self.price = self.original_price - (self.original_price * self.discount_percent / 100)
        else:
            self.price = self.original_price
        super().save(*args, **kwargs)

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            name="Тест",
        )

    class Meta:
        db_table = "products"
        verbose_name = _("Продукт")
        verbose_name_plural = _("Продукты")


class ProductsimageModel(AbstractBaseModel):
    product = models.ForeignKey(
        ProductsModel,
        verbose_name=_("Продукт"),
        on_delete=models.CASCADE,
        related_name="images",
        null=True,
        blank=True
    )
    image = models.ImageField(_("Изображение"), upload_to="product-image/")

    def __str__(self):
        return self.product.name

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            name="Тест",
        )

    class Meta:
        db_table = "productsImage"
        verbose_name = _("Изображение продукта")
        verbose_name_plural = _("Изображения продукта")
