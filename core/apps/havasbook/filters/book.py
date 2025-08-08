# core/apps/havasbook/filters/book.py

import django_filters
from decimal import Decimal
from django.db.models import Q
from core.apps.havasbook.models import BookModel
from core.apps.havasbook.serializers.book.currency import convert_currency



class BookFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_by_search', label='Qidiruv')
    gender = django_filters.CharFilter(method="filter_by_gender", label="Jins")
    brand = django_filters.NumberFilter(field_name='brand_id', label='Brend ID')
    category = django_filters.NumberFilter(field_name='subcategory__category_id', label='Kategoriya ID')
    subcategory = django_filters.NumberFilter(field_name='subcategory_id', label='Subkategoriya ID')

    min_price = django_filters.NumberFilter(method='filter_min_price', label='Minimal narx')
    max_price = django_filters.NumberFilter(method='filter_max_price', label='Maksimal narx')

    min_sold_count = django_filters.NumberFilter(field_name='sold_count', lookup_expr='gte', label='Minimal sotilgan')
    max_sold_count = django_filters.NumberFilter(field_name='sold_count', lookup_expr='lte', label='Maksimal sotilgan')

    is_discount = django_filters.BooleanFilter(field_name='is_discount', label='Chegirmadami')
    is_preorder = django_filters.BooleanFilter(field_name='is_preorder', label='Oldindan buyurtmadami')
    popular = django_filters.BooleanFilter(method='filter_by_popular', label='Ommabopmi')

    ordering = django_filters.OrderingFilter(
        fields=(
            ('sold_count', 'sold_count'),
            ('view_count', 'view_count'),
            ('created_at', 'created_at'),
            ('price', 'price'),
            ('name', 'name'),
            ('popular', 'popular'),
        ),
        field_labels={
            'sold_count': 'Sotilganlar',
            'view_count': 'Ko‘rishlar',
            'created_at': 'Yaratilgan sana',
            'price': 'Narx',
            'name': 'Nomi',
            'popular': 'Ommabop',
        },
        label="Saralash"
    )

    class Meta:
        model = BookModel
        fields = [
            'search', 'gender', 'brand',
            'category', 'subcategory',
            'min_price', 'max_price',
            'min_sold_count', 'max_sold_count',
            'is_discount', 'is_preorder',
            'popular'
        ]

    # Context-based initialization (for currency)
    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        super().__init__(data, queryset, request=request, prefix=prefix)
        self.request = request
        self.currency = request.headers.get("currency") if request else None

    def filter_by_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(description__icontains=value)
        )

    def filter_by_gender(self, queryset, name, value):
        return queryset.filter(
            Q(gender__gender=value) | Q(gender__gender="unisex")
        )

    def filter_min_price(self, queryset, name, value):
        try:
            value = Decimal(str(value))
            usd_price = self.convert_to_usd(value)
            return queryset.filter(price__gte=usd_price)
        except:
            return queryset

    def filter_max_price(self, queryset, name, value):
        try:
            value = Decimal(str(value))
            usd_price = self.convert_to_usd(value)
            return queryset.filter(price__lte=usd_price)
        except:
            return queryset

    def filter_by_popular(self, queryset, name, value):
        return queryset.filter(popular=value)

    def convert_to_usd(self, value: Decimal) -> Decimal:
        if not self.currency or self.currency.upper() == "USD":
            return value
        rate = convert_currency(Decimal(1), self.currency.upper())
        if rate == 0:
            return value
        return round(value / rate, 2)
