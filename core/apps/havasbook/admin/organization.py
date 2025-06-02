from django.contrib import admin
from unfold.admin import ModelAdmin

from core.apps.havasbook.models import OrganizationModel


@admin.register(OrganizationModel)
class OrganizationAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )
