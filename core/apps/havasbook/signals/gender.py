from django.db.models.signals import post_save
from django.dispatch import receiver

from core.apps.havasbook.models import GenderModel


@receiver(post_save, sender=GenderModel)
def GenderSignal(sender, instance, created, **kwargs): ...
