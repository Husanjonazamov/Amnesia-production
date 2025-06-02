from django.contrib import admin
from unfold.admin import ModelAdmin

from ..models import DeliveryModel
from modeltranslation.admin import TabbedTranslationAdmin


@admin.register(DeliveryModel)
class DeliveryAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = (
        "id",
        "__str__",
    )
