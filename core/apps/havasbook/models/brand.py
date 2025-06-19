from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel



class BrandModel(AbstractBaseModel):
    name = models.CharField(
        verbose_name=_("Brand"), 
        max_length=255
    )
    

    def __str__(self):
        return self.name

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            name="mock",
        )

    class Meta:
        db_table = "brand"
        verbose_name = _("BrandModel")
        verbose_name_plural = _("BrandModels")
