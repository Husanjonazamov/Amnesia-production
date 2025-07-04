from django.contrib import admin
from unfold.admin import ModelAdmin
from modeltranslation.admin import TabbedTranslationAdmin


from ..models import CategoryModel


@admin.register(CategoryModel)
class CategoryAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = (
        "id",
        "__str__",
    )
    
    search_fields = ['name', 'gender__gender']
