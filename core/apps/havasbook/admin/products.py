from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from ..models import ProductsimageModel, ProductsModel

from modeltranslation.admin import TabbedTranslationAdmin



class ProductImageInline(TabularInline):
    model = ProductsimageModel
    extra = 1 



@admin.register(ProductsModel)
class ProductsAdmin(ModelAdmin, TabbedTranslationAdmin):
    readonly_fields = ("price",)
    list_display = (
        "id",
        "__str__",
        'name',
        'price',
        'quantity',
        'is_discount',
    )
    
    list_filter = ('is_discount',)
    search_fields = ('original_price',)


    def save_model(self, request, obj, form, change):
        if obj.is_discount and obj.discount_percent is not None:
            obj.price = obj.original_price - (obj.original_price * obj.discount_percent / 100)
        else:
            obj.price = obj.original_price  # Chegirma yo'q bo'lsa, original_price'ni saqlaydi
        super().save_model(request, obj, form, change)
        
        
    inlines = [
        ProductImageInline,
    ]

@admin.register(ProductsimageModel)
class ProductsimageAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
        'product_name',
        'product_is_discount'
    )
    
    def product_name(self, obj):
        return obj.product.name if obj.product else "product Topilmadi"
    
    def product_is_discount(self, obj):
        return obj.product.is_discount if obj.product else "Narx nomalum"
    
