from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin, TabularInline

from ..models import BookimageModel, BookModel


class BookimageInline(TabularInline):
    model = BookimageModel
    extra = 1


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

    list_filter = ('is_discount', "created_at", )
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
