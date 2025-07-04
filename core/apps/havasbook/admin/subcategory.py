from django.contrib import admin
from unfold.admin import ModelAdmin

from core.apps.havasbook.models import SubcategoryModel


@admin.register(SubcategoryModel)
class SubcategoryAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )


    search_fields = ['name', 'category__gender__gender']
    
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term.lower() in ['male', 'female']: 
            queryset = queryset.filter(category__gender__gender__iexact=search_term)

        return queryset, use_distinct
