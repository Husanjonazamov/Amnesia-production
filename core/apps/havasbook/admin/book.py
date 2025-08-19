from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin, TabularInline

from ..models import BookimageModel, BookModel
from django.contrib.admin import DateFieldListFilter


from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import timedelta


class BookimageInline(TabularInline):
    model = BookimageModel
    extra = 1





class CreatedAtMonthFilter(SimpleListFilter):
    title = _('Month')
    parameter_name = 'month'

    def lookups(self, request, model_admin):
        """
        Joriy yil bo‘yicha 1 (Yanvar) dan 12 (Dekabr) gacha oylarni chiqaradi
        """
        today = timezone.now().date()
        year = today.year
        months = []
        for m in range(1, 13):
            month_date = today.replace(month=m, day=1)
            months.append((
                f"{year}-{m:02d}",   # filter value
                month_date.strftime("%B %Y")  # label (Yanvar 2025, Fevral 2025, ...)
            ))
        return months

    def queryset(self, request, queryset):
        if self.value():
            year, month = map(int, self.value().split('-'))
            return queryset.filter(created_at__year=year, created_at__month=month)
        return queryset




@admin.register(BookModel)
class BookAdmin(ModelAdmin, TabbedTranslationAdmin):
    readonly_fields = ("price",)
    list_display = (
        "id",
        "__str__",
        'name',
        'price',
        "category",
        "get_subcategory",
        'quantity',
        "created_at",
        'is_discount',
    )

    list_filter = ('is_discount', CreatedAtMonthFilter,)

    search_fields = ('original_price',)
    autocomplete_fields = ['brand', 'category', 'subcategory']

    def get_subcategory(self, obj):
        if obj.category and hasattr(obj.category, "subcategories"):
           subs = obj.category.subcategories.all()
           return ", ".join([s.name for s in subs]) if subs.exists() else None
        return None

    get_subcategory.short_description = "Подкатегория"


    
    def save_model(self, request, obj, form, change):
        if obj.is_discount and obj.discount_percent is not None:
            obj.price = obj.original_price - (obj.original_price * obj.discount_percent / 100)
        else:
            obj.price = obj.original_price
        super().save_model(request, obj, form, change)

    inlines = [BookimageInline]


@admin.register(BookimageModel)
class BookimageAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
        'book_name',
        'book_is_discount',
    )

    def book_name(self, obj):
        return obj.book.name if obj.book else "Kitob Topilmadi"
    book_name.short_description = "Kitob nomi"

    def book_is_discount(self, obj):
        return obj.book.is_discount if obj.book else "Chegirma yo‘q"
    book_is_discount.short_description = "Chegirma"
