from django.contrib import admin
from unfold.admin import ModelAdmin

from core.apps.havasbook.models import GenderModel


@admin.register(GenderModel)
class GenderAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )
