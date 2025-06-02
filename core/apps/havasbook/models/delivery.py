from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel


class DeliveryModel(AbstractBaseModel):
    title = models.CharField(_("Nomi"), max_length=255)
    price = models.IntegerField(_("Narxi"), default=0, null=True, blank=True)

    def __str__(self):
        return self.title

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            name="Test",
        )

    class Meta:
        db_table = "delivery"
        verbose_name = _("DeliveryModel")
        verbose_name_plural = _("DeliveryModels")
