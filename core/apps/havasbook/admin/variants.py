from django.contrib import admin
from unfold.admin import ModelAdmin
from modeltranslation.admin import TabbedTranslationAdmin


from ..models import ColorModel, SizeModel


@admin.register(ColorModel)
class ColorAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = (
        "id",
        "__str__",
    )
    search_fields = ['title']
    


@admin.register(SizeModel)
class SizeAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = (
        "id",
        "__str__",
    )

    search_fields = ['title']
