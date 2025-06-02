from modeltranslation.translator import TranslationOptions, register

from ..models import CategoryModel


@register(CategoryModel)
class CategoryTranslation(TranslationOptions):
    fields = [
        'name'
    ]
