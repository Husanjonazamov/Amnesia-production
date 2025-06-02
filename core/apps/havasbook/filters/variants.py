from django_filters import rest_framework as filters

from ..models import ColorModel, SizeModel


class ColorFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = ColorModel
        fields = ("name",)


class SizeFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = SizeModel
        fields = ("name",)
