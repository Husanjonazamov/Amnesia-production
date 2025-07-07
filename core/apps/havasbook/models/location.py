from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel
from geopy.geocoders import Nominatim


class LocationModel(AbstractBaseModel):
    title = models.CharField(_("Название"), max_length=255, null=True, blank=True)
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="locations",
        blank=True,
        null=True
    ) 
    lat = models.FloatField(_("Широта"))  # Kenglik
    long = models.FloatField(_("Долгота"))  # Uzunlik

    def __str__(self):
        return self.title or "tile" 
    
    def get_address(self):
        geolocator = Nominatim(user_agent="myapp")
        location = geolocator.reverse((self.latitude, self.longitude), language='ru')
        if location:
            return location.address
        return _("Адрес не найден")

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.get_address()
        super(LocationModel, self).save(*args, **kwargs)

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            name="Тест",
        )

    class Meta:
        db_table = "location"
        verbose_name = _("Локация")
        verbose_name_plural = _("Локации")
