import django_filters
from core.apps.havasbook.models.preorder import PreorderModel, Status

class PreorderFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(
        choices=Status.choices, 
        label="Status"
    )
    reciever_name = django_filters.CharFilter(lookup_expr='icontains', label="Foydalanuvchi ismi")

    class Meta:
        model = PreorderModel
        fields = ['status', 'reciever_name']
 