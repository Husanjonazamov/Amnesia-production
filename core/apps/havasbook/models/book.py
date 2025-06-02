from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel
from django.utils.html import mark_safe

from django.db import models
from django.utils.translation import gettext_lazy as _


class ProductTypeChoice(models.TextChoices):
    BOOK = 'book', _('Kitob')
    CLOTHES = 'clothes', _('Kiyim')
    TECHNIQUE = 'technique', _('Texnika')
    OTHER = 'other', _('Boshqalar')



class CurrencyChoices(models.TextChoices):
    USD = 'USD', _('$')
    UZS = 'UZS', _("so'm")
    RUB = 'RUB', _('₽')
    EUR = 'EUR', _('€')
    
class GenderChoices(models.TextChoices):
    MALE = "male", "Erkaklar uchun"
    FEMALE = "female", "Ayollar uchun"
    UNISEX = "unisex", "Ikkalasiga ham"



class BookModel(AbstractBaseModel):
    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("Mahsulot tavsifi"), null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
        default=GenderChoices.UNISEX,
    )
    category = models.ForeignKey(
        "havasbook.CategoryModel",
        verbose_name=_("Kategoriylar"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books'
    )
    color = models.ManyToManyField(
        'havasbook.ColorModel',
        verbose_name=_("Mahsulot Rangi"),
        blank=True
    )
    size = models.ManyToManyField(
        'havasbook.SizeModel',
        verbose_name=_("O'lchami"),
        blank=True
    )
    image = models.ImageField(_("Rasm"), upload_to="book-image/", null=True, blank=True)
    
    base_currency = models.CharField(
        _("Asosiy valyuta"),
        max_length=3,
        choices=CurrencyChoices.choices,
        default=CurrencyChoices.USD
    )
    
    original_price = models.DecimalField(
        _("Asl narxi"), max_digits=10, decimal_places=2, null=True, blank=True
    )
    price = models.DecimalField(
        _("Chegirmadagi narxi"), max_digits=10, decimal_places=2, null=True, blank=True
    )
    is_discount = models.BooleanField(_("Chegirma bormi ?"), default=False)
    discount_percent = models.DecimalField(
        _("chegirma foizi"), max_digits=10, decimal_places=2, null=True, blank=True
    )
    
    book_id = models.CharField(
        verbose_name=_("Kitob id"),
        max_length=155,
        blank=True,
        null=True
    )

    quantity = models.PositiveIntegerField(
        _("Kitob soni"), default=0, null=True, blank=True
    )
    
    sold_count = models.PositiveIntegerField(  
        _("Sotilganlar soni"),
        default=0
    )

    view_count = models.PositiveIntegerField(
        _("Ko'rishlar soni"),
        default=0
    )
    popular = models.BooleanField(
        _("Mashhurmi ?"),
        default=False
    )

    is_preorder = models.BooleanField(  
        _("Oldindan buyurtma bormi?"),
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
            name="Test",
        )

    class Meta:
        db_table = "book"
        verbose_name = _("BookModel")
        verbose_name_plural = _("BookModels")




class BookimageModel(AbstractBaseModel):
    book = models.ForeignKey(
        BookModel, 
        verbose_name=_("Kitob"), 
        on_delete=models.CASCADE,
        related_name="images",
        null=True, 
        blank=True
    )
    image = models.ImageField(_("Rasm"),  upload_to="book-image/")
   

    def __str__(self):
        return self.book.name or 'Kitob rasmlari'

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            name="Test",
        )

    class Meta:
        db_table = "bookImage"
        verbose_name = _("BookimageModel")
        verbose_name_plural = _("BookimageModels")
