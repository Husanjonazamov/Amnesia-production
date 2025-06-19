from django_filters import rest_framework as filters

from core.apps.havasbook.models import SubcategoryModel


class SubcategoryFilter(filters.FilterSet):
    # name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = SubcategoryModel
        fields = [
            "name",
        ]
