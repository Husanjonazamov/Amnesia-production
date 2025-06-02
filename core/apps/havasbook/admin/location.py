from django.contrib import admin
from unfold.admin import ModelAdmin

from ..models import LocationModel
from modeltranslation.admin import TabbedTranslationAdmin

from django.utils.translation import gettext_lazy as _

@admin.register(LocationModel)
class LocationAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = (
        "id",
        'title',
        'get_title',
        'long',
        'lat'
    )


    def get_title(self, obj):
        return obj.title if obj.title else _("No title")