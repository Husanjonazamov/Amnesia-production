from django.contrib import admin
from unfold.admin import ModelAdmin

from ..models import CartitemModel, CartModel


@admin.register(CartModel)
class CartAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
        "user_name",
        'total_price'
    )
    
    def user_name(self, obj):
        return obj.user.first_name


@admin.register(CartitemModel)
class CartitemAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )
