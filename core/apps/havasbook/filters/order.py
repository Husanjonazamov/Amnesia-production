from django_filters import rest_framework as filters

from ..models import OrderModel, OrderStatus


class OrderFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    status = filters.ChoiceFilter(choices=OrderStatus.choices, label="Order Status")

    class Meta:
        model = OrderModel
        fields = ("name", "status",)
