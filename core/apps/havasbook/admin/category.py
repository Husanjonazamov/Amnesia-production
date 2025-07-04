from django.contrib import admin
from unfold.admin import ModelAdmin
from modeltranslation.admin import TabbedTranslationAdmin


from ..models import CategoryModel


@admin.register(CategoryModel)
class CategoryAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = (
        "id",
        "__str__",
    )
    
    search_fields = ['name', 'gender__gender']
    
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term.lower() in ['male', 'female']: 
            queryset = queryset.filter(gender__gender__iexact=search_term)

        return queryset, use_distinct
