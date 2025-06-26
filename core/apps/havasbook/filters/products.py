from django_filters import rest_framework as filters

from ..models import ProductsimageModel, ProductsModel


class ProductsFilter(filters.FilterSet):
    price_min = filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = filters.NumberFilter(field_name="price", lookup_expr="lte")
    brand = filters.NumberFilter(field_name="brand__id")
    
    ordering = filters.OrderingFilter(
        fields=(
            ("price", "price"),
            ("sold_count", "sold_count"),
            ("view_count", "view_count"),
        ),
        field_labels={
            "price": "Narx",
            "sold_count": "Sotilganlar soni",
            "view_count": "Ko‘rishlar soni",
        }
    )

    class Meta:
        model = ProductsModel
        fields = ["category", "brand", "is_discount", "is_preorder"]


class ProductsimageFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = ProductsimageModel
        fields = ("name",)
