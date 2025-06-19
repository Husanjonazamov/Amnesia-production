from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel


class SubcategoryModel(AbstractBaseModel):
    name = models.CharField(verbose_name=_("name"), max_length=255)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='children'
    )
    category = models.ForeignKey(
        "havasbook.CategoryModel",
        on_delete=models.CASCADE,
        verbose_name=_("Cateogry"),
        blank=True, null=True
    )
    


    def __str__(self):
        return self.name

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            name="mock",
        )

    class Meta:
        db_table = "subcategory"
        verbose_name = _("SubcategoryModel")
        verbose_name_plural = _("SubcategoryModels")
