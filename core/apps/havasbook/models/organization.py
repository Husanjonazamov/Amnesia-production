from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel


class OrganizationModel(AbstractBaseModel):
    name = models.CharField(
        verbose_name=_("Ism"),
        max_length=255,
    )
    phone = models.CharField(
        verbose_name=_("Telefon raqam"),
        max_length=20,
        blank=True, 
        null=True
    )
    bot_token = models.CharField(   
        verbose_name=_("Token"),
        max_length=200, 
        blank=True, 
        null=True
    ) 

    def __str__(self):
        return self.pk

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            name="mock",
        )

    class Meta:
        db_table = "Organization"
        verbose_name = _("OrganizationModel")
        verbose_name_plural = _("OrganizationModels")
