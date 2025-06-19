from django.contrib import admin
from unfold.admin import ModelAdmin

from core.apps.havasbook.models import SubcategoryModel


@admin.register(SubcategoryModel)
class SubcategoryAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )
