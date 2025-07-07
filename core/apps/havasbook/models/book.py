from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel
from django.utils.html import mark_safe


class ProductTypeChoice(models.TextChoices):
    BOOK = 'book', _('Книга')
    CLOTHES = 'clothes', _('Одежда')
    TECHNIQUE = 'technique', _('Техника')
    OTHER = 'other', _('Другие')


class CurrencyChoices(models.TextChoices):
    USD = 'USD', _('Доллар США ($)')
    UZS = 'UZS', _("Сум (UZS)")
    RUB = 'RUB', _('Рубль (₽)')
    EUR = 'EUR', _('Евро (€)')


class BookModel(AbstractBaseModel):
    name = models.CharField(_("Название"), max_length=255)
    description = models.TextField(_("Описание товара"), null=True, blank=True)
    gender = models.ForeignKey(
        "havasbook.GenderModel",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_("Пол")
    )
    brand = models.ForeignKey(
        "havasbook.BrandModel",
        on_delete=models.CASCADE,
        verbose_name=_("Бренд"),
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        "havasbook.CategoryModel",
        verbose_name=_("Категория"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books'
    )
    subcategory = models.ForeignKey(
        "havasbook.SubCategoryModel",
        on_delete=models.CASCADE,
        verbose_name=_("Подкатегория"),
        blank=True,
        null=True
    )
    color = models.ManyToManyField(
        "havasbook.ColorModel",
        verbose_name=_("Цвет товара"),
        blank=True
    )
    size = models.ManyToManyField(
        "havasbook.SizeModel",
        verbose_name=_("Размер"),
        blank=True
    )
    image = models.ImageField(_("Изображение"), upload_to="book-image/", null=True, blank=True)

    base_currency = models.CharField(
        _("Основная валюта"),
        max_length=3,
        choices=CurrencyChoices.choices,
        default=CurrencyChoices.USD
    )
    original_price = models.DecimalField(_("Исходная цена"), max_digits=10, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(_("Цена со скидкой"), max_digits=10, decimal_places=2, null=True, blank=True)
    is_discount = models.BooleanField(_("Есть скидка?"), default=False)
    discount_percent = models.DecimalField(_("Процент скидки (%)"), max_digits=10, decimal_places=2, null=True, blank=True)

    book_id = models.CharField(_("ID товара"), max_length=155, blank=True, null=True)
    quantity = models.PositiveIntegerField(_("Количество на складе"), default=0, null=True, blank=True)
    sold_count = models.PositiveIntegerField(_("Продано (шт.)"), default=0)
    view_count = models.PositiveIntegerField(_("Количество просмотров"), default=0)
    popular = models.BooleanField(_("Популярный?"), default=False)
    is_preorder = models.BooleanField(_("Доступен предзаказ?"), default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.discount_percent is not None and self.original_price:
            self.price = self.original_price - (self.original_price * self.discount_percent / 100)
        else:
            self.price = self.original_price
        super().save(*args, **kwargs)

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            name="Тестовый товар",
        )

    class Meta:
        db_table = "book"
        verbose_name = _("Товар")
        verbose_name_plural = _("Товары")


class BookimageModel(AbstractBaseModel):
    book = models.ForeignKey(
        BookModel,
        verbose_name=_("Товар"),
        on_delete=models.CASCADE,
        related_name="images",
        null=True,
        blank=True
    )
    image = models.ImageField(_("Изображение"), upload_to="book-image/")

    def __str__(self):
        return self.book.name or 'Изображение товара'

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            name="Тестовое изображение",
        )

    class Meta:
        db_table = "bookImage"
        verbose_name = _("Изображение товара")
        verbose_name_plural = _("Изображения товаров")
