from modeltranslation.translator import TranslationOptions, register

from ..models import BookimageModel, BookModel

@register(BookModel)
class BookTranslation(TranslationOptions):
    fields = [
        "name",
        "description"
    ]


@register(BookimageModel)
class BookimageTranslation(TranslationOptions):
    fields = []
