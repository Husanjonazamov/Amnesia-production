from modeltranslation.translator import TranslationOptions, register

from core.apps.havasbook.models import OrganizationModel


class OrganizationTranslation(TranslationOptions):
    fields = ()


@register(OrganizationModel)
class OrganizationTranslation(TranslationOptions):
    fields = []
