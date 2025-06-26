import django_filters
from django.db.models import Q
from core.apps.havasbook.models import BookModel


class BookFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='Min Price')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='Max Price')
    min_sold_count = django_filters.NumberFilter(field_name='sold_count', lookup_expr='gte', label='Min Sold Count')
    max_sold_count = django_filters.NumberFilter(field_name='sold_count', lookup_expr='lte', label='Max Sold Count')
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains', label='Category')
    is_discount = django_filters.BooleanFilter(field_name='is_discount', label='Discounted Books')
    is_preorder = django_filters.BooleanFilter(field_name='is_preorder', label='Pre-order Books')
    
    gender = django_filters.CharFilter(method="filter_by_gender")
    brand = django_filters.CharFilter(method="brand_id")

    search = django_filters.CharFilter(method='filter_by_search', label='Search Books')
    popular = django_filters.BooleanFilter(method='filter_by_popular', label='Popular Books')
    subcategory = django_filters.NumberFilter(field_name='subcategory_id')


    def filter_by_gender(self, queryset, name, value):
        return queryset.filter(
            Q(gender__gender=value) | Q(gender__gender="unisex")
        )



    def filter_by_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(description__icontains=value)
        )

    def filter_by_popular(self, queryset, name, value):
        if value:
            queryset = queryset.filter(popular=True)
        return queryset

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
            'view_count': 'Ko\'rishlar',
            'created_at': 'Yaratilgan sana',
            'price': 'Narx',
            'name': 'Nomi',
            'popular': 'Ommaboplik (popular=True oldin chiqadi)',
            'type': 'Mahsulot turi',
        },
        label="Saralash tartibi"
    )

    class Meta:
        model = BookModel
        fields = [
            'min_price',
            'max_price',
            'min_sold_count',
            'max_sold_count',
            'category',
            'is_discount',
            'is_preorder',
            'popular',
            'search',
            'gender', 
            "brand",
            "subcategory"
        ]
