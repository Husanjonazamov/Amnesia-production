from django.contrib import admin
from unfold.admin import ModelAdmin

from core.apps.havasbook.models import SubcategoryModel
from django.db import models
from modeltranslation.admin import TabbedTranslationAdmin



@admin.register(SubcategoryModel)
class SubcategoryAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = (
        "id",
        "__str__",
    )


    search_fields = ['name', 'category__gender__gender', "category__name"]
    
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term:
            if search_term.lower() in ['male', 'female']:
                queryset = queryset.filter(category__gender__gender__iexact=search_term)

            queryset = queryset.filter(
                models.Q(category__name__icontains=search_term) |
                models.Q(name__icontains=search_term)
            )

        return queryset.distinct(), use_distinct