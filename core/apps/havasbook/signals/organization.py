from django.db.models.signals import post_save
from django.dispatch import receiver

from core.apps.havasbook.models import OrganizationModel


@receiver(post_save, sender=OrganizationModel)
def OrganizationSignal(sender, instance, created, **kwargs): ...
