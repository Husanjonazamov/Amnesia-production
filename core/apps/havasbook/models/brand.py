from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel

class BrandModel(AbstractBaseModel):
    name = models.CharField(
        verbose_name=_("Бренд"), 
        max_length=255
    )
    gender = models.ForeignKey("havasbook.GenderModel", on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to="brands/", blank=True, null=True)

    categories = models.ManyToManyField(
        "havasbook.CategoryModel",
        verbose_name=_("Категория"),
        blank=True,
        related_name="brands"  
    )

    subcategories = models.ManyToManyField(
        "havasbook.SubcategoryModel", related_name="brands", blank=True
    )
    

    category = models.ForeignKey(
        "havasbook.CategoryModel",
        on_delete=models.CASCADE,
        verbose_name=_("Категория"),
        blank=True,
        null=True,
        related_name="main_brands" 
    )
    has_products = models.BooleanField(default=False, verbose_name=_("Mahsulot borligi"))

    
    def __str__(self):
        return f"{self.name}-{self.gender.gender}"

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            name="mock",
        )

    class Meta:
        db_table = "brand"
        verbose_name = _("Бренд")
        verbose_name_plural = _("Бренды")
