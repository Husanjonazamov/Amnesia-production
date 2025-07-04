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
        'quantity',
        "book_id",
        'is_discount',
    )
    
    list_filter = ('is_discount',)
    filter_horizontal = ('color', 'size')
    search_fields = ('original_price',)
    autocomplete_fields = ['brand', 'category', 'subcategory']

    

    def save_model(self, request, obj, form, change):
        if obj.is_discount and obj.discount_percent is not None:
            obj.price = obj.original_price - (obj.original_price * obj.discount_percent / 100)
        else:
            obj.price = obj.original_price  # Chegirma yo'q bo'lsa, original_price'ni saqlaydi
        super().save_model(request, obj, form, change)
        
        
    inlines = [
        BookimageInline,
    ]

@admin.register(BookimageModel)
class BookimageAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
        'book_name',
        'book_is_discount'
    )
    
    def book_name(self, obj):
        return obj.book.name if obj.book else "Kitob Topilmadi"
    
    def book_is_discount(self, obj):
        return obj.book.is_discount if obj.book else "Narx nomalum"
    
