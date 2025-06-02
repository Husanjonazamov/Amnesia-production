from django.contrib import admin
from unfold.admin import ModelAdmin

from ..models import PreorderModel


@admin.register(PreorderModel)
class PreorderAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )
