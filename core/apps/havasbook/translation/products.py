from modeltranslation.translator import TranslationOptions, register

from ..models import ProductsimageModel, ProductsModel


@register(ProductsModel)
class ProductsTranslation(TranslationOptions):
    fields = [
        'name',
        'description'
    ]


@register(ProductsimageModel)
class ProductsimageTranslation(TranslationOptions):
    fields = []
