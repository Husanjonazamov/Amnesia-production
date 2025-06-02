from modeltranslation.translator import TranslationOptions, register

from ..models import DeliveryModel


@register(DeliveryModel)
class DeliveryTranslation(TranslationOptions):
    fields = [
        'title'
    ]
