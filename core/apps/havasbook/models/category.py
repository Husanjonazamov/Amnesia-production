from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel


class CategoryModel(AbstractBaseModel):
    name = models.CharField(_("Название"), max_length=255)
    gender = models.ForeignKey(
        "havasbook.GenderModel",
        on_delete=models.CASCADE,
        blank=True, null=True,
        verbose_name=_("Пол")
    )
   
    image = models.ImageField(_("Изображение"), upload_to="category-image/")
    
    def __str__(self):
        return f"{self.name}-{self.gender.gender}"

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            name="Test",
        )

    class Meta:
        db_table = "category"
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")
