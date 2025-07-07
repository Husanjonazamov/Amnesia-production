from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel


class SubcategoryModel(AbstractBaseModel):
    name = models.CharField(verbose_name=_("Название"), max_length=255)
    category = models.ForeignKey(
        "havasbook.CategoryModel",
        on_delete=models.CASCADE,
        verbose_name=_("Категория"),
        blank=True, null=True
    )

    def __str__(self):
        return f"{self.name}-{self.category.gender.gender}"

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            name="Тест",
        )

    class Meta:
        db_table = "subcategory"
        verbose_name = _("Подкатегория")
        verbose_name_plural = _("Подкатегории")
