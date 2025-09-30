from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel


class ChildcategoryModel(AbstractBaseModel):
    title = models.CharField(_("Название"), max_length=255)
    subcategory = models.ForeignKey("havasbook.SubcategoryModel", on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.title}-{self.subcategory.category.gender.gender}"

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            name="mock",
        )

    class Meta:
        db_table = "ChildCategory"
        verbose_name = _("ChildcategoryModel")
        verbose_name_plural = _("ChildcategoryModels")
