from django_filters import rest_framework as filters

from ..models import ProductsimageModel, ProductsModel


class ProductsFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = ProductsModel
        fields = ("name",)


class ProductsimageFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = ProductsimageModel
        fields = ("name",)
