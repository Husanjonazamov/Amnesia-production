from django.db.models.signals import post_save
from django.dispatch import receiver

from ..models import BannerModel


@receiver(post_save, sender=BannerModel)
def BannerSignal(sender, instance, created, **kwargs): ...
