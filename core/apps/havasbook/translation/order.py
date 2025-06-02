from modeltranslation.translator import TranslationOptions, register

from ..models import OrderitemModel, OrderModel


@register(OrderModel)
class OrderTranslation(TranslationOptions):
    fields = []


@register(OrderitemModel)
class OrderitemTranslation(TranslationOptions):
    fields = []
