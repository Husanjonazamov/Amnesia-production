from modeltranslation.translator import TranslationOptions, register

from ..models import ColorModel, SizeModel


@register(ColorModel)
class ColorTranslation(TranslationOptions):
    fields = [
        'title',
        'name'
    ]


@register(SizeModel)
class SizeTranslation(TranslationOptions):
    fields = [
        'title',
        'name'
    ]


