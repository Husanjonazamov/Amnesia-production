from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel


class GenderChoices(models.TextChoices):
    MALE = "male", _("Для мужчин")
    FEMALE = "female", _("Для женщин")
    UNISEX = "unisex", _("Для всех")


class GenderModel(AbstractBaseModel):
    gender = models.CharField(
        verbose_name=_("Пол"),
        max_length=255,
        choices=GenderChoices.choices,
        default=GenderChoices.MALE
    )

    def __str__(self):
        return self.gender

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            name="mock",
        )

    class Meta:
        db_table = "gender"
        verbose_name = _("Пол")
        verbose_name_plural = _("Полы")
