from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel


class ColorModel(AbstractBaseModel):
    title = models.CharField(_("Цвет"))
    name = models.CharField(_("Название цвета"), max_length=50)
    image = models.ImageField(_("Изображение цвета"), upload_to="book-color/")

    def __str__(self):
        return self.name

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            name="Тест",
        )

    class Meta:
        db_table = "color"
        verbose_name = _("Цвет")
        verbose_name_plural = _("Цвета")


class SizeModel(AbstractBaseModel):
    title = models.CharField(_("Размер"))
    name = models.CharField(_("Название размера"), max_length=255)

    def __str__(self):
        return self.name

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            name="Тест",
        )

    class Meta:
        db_table = "size"
        verbose_name = _("Размер")
        verbose_name_plural = _("Размеры")
