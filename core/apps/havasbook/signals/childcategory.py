from django.db.models.signals import post_save
from django.dispatch import receiver

from core.apps.havasbook.models import ChildcategoryModel


@receiver(post_save, sender=ChildcategoryModel)
def ChildcategorySignal(sender, instance, created, **kwargs): ...
