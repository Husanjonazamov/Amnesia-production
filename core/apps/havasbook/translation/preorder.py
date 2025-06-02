from modeltranslation.translator import TranslationOptions, register

from ..models import PreorderModel


@register(PreorderModel)
class PreorderTranslation(TranslationOptions):
    fields = []
