from modeltranslation.translator import TranslationOptions, register

from core.apps.havasbook.models import ChildcategoryModel


@register(ChildcategoryModel)
class ChildcategoryTranslation(TranslationOptions):
    fields = [
        "title"
    ]
