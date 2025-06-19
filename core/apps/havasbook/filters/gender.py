from django_filters import rest_framework as filters

from core.apps.havasbook.models import GenderModel


class GenderFilter(filters.FilterSet):
    # name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = GenderModel
        fields = [
            "name",
        ]
