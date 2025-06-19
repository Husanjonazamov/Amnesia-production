from django_filters import rest_framework as filters

from core.apps.havasbook.models import GenderModel


class GenderFilter(filters.FilterSet):
    gender = filters.CharFilter(field_name="gender", lookup_expr="icontains")

    class Meta:
        model = GenderModel
        fields = [
            "gender",
        ]
