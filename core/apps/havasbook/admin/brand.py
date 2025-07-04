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
    
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term.lower() in ['male', 'female']: 
            queryset = queryset.filter(gender__gender__iexact=search_term)

        return queryset, use_distinct
