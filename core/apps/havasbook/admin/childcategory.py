from django.contrib import admin
from unfold.admin import ModelAdmin
from modeltranslation.admin import TabbedTranslationAdmin


from core.apps.havasbook.models import ChildcategoryModel


@admin.register(ChildcategoryModel)
class ChildcategoryAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = (
        "id",
        "title",
    )
    
    search_fields = ['title', ]
    autocomplete_fields = ['subcategory']
