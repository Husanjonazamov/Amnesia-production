from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel
from geopy.geocoders import Nominatim


class LocationModel(AbstractBaseModel):
    title = models.CharField(_("name"), max_length=255, null=True, blank=True)
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="locations", blank=True, null=True) 
    lat = models.FloatField(
        _("Kenglik"),
    )
    long = models.FloatField(
        _("Uzunlik"),
    )

    def __str__(self):
        return self.title or "tile" 
    
    def get_address(self):
        geolocator = Nominatim(user_agent="myapp")
        location = geolocator.reverse((self.latitude, self.longitude), language='en')
        if location:
            return location.address
        return _("Address not found")

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.get_address()
        super(LocationModel, self).save(*args, **kwargs)

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            name="Test",
        )

    class Meta:
        db_table = "location"
        verbose_name = _("LocationModel")
        verbose_name_plural = _("LocationModels")
