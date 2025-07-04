from django.contrib import admin
from unfold.admin import ModelAdmin

from core.apps.havasbook.models import BrandModel


@admin.register(BrandModel)
class BrandAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )
    
    autocomplete_fields = ['category']
    search_fields = ['name', 'gender__gender']
