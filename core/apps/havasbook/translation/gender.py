from modeltranslation.translator import TranslationOptions, register

from core.apps.havasbook.models import GenderModel


@register(GenderModel)
class GenderTranslation(TranslationOptions):
    fields = []
