from modeltranslation.translator import TranslationOptions, register

from core.apps.havasbook.models import BrandModel


@register(BrandModel)
class BrandTranslation(TranslationOptions):
    fields = []
