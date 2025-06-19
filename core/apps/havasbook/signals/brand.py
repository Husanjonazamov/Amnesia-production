from django.db.models.signals import post_save
from django.dispatch import receiver

from core.apps.havasbook.models import BrandModel


@receiver(post_save, sender=BrandModel)
def BrandSignal(sender, instance, created, **kwargs): ...
