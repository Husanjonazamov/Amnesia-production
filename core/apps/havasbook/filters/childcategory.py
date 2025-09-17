from django_filters import rest_framework as filters

from core.apps.havasbook.models import ChildcategoryModel


class ChildcategoryFilter(filters.FilterSet):
    # name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = ChildcategoryModel
        fields = [
            "title",
        ]
