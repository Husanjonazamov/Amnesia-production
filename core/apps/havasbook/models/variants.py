from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel


class ColorModel(AbstractBaseModel):
    title = models.CharField(_("Rang"))
    name = models.CharField(_("Rang Nomi"), max_length=50)
    image = models.ImageField(_("Rangi"), upload_to="book-color/")


    def __str__(self):
        return self.name

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            name="Test",
        )

    class Meta:
        db_table = "color"
        verbose_name = _("ColorModel")
        verbose_name_plural = _("ColorModels")


class SizeModel(AbstractBaseModel):
    title = models.CharField(_("O'lcham"))
    name = models.CharField(_("O'lcham nomi"), max_length=255)

    def __str__(self):
        return self.name

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            name="Test",
        )

    class Meta:
        db_table = "size"
        verbose_name = _("SizeModel")
        verbose_name_plural = _("SizeModels")

