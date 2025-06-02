from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel



class CategoryModel(AbstractBaseModel):
    name = models.CharField(_("name"), max_length=255)
    image = models.ImageField(_("Rasm"), upload_to="category-image/")

    def __str__(self):
        return self.name

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            name="Test",
        )

    class Meta:
        db_table = "category"
        verbose_name = _("CategoryModel")
        verbose_name_plural = _("CategoryModels")
