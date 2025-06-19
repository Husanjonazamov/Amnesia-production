from modeltranslation.translator import TranslationOptions, register

from core.apps.havasbook.models import SubcategoryModel


@register(SubcategoryModel)
class SubcategoryTranslation(TranslationOptions):
    fields = []
