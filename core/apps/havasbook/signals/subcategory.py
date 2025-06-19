from django.db.models.signals import post_save
from django.dispatch import receiver

from core.apps.havasbook.models import SubcategoryModel


@receiver(post_save, sender=SubcategoryModel)
def SubcategorySignal(sender, instance, created, **kwargs): ...
