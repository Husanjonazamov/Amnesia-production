from django.contrib import admin
from unfold.admin import ModelAdmin

from ..models import OrderitemModel, OrderModel


@admin.register(OrderModel)
class OrderAdmin(ModelAdmin):
    list_display = (
        "id",
        # '__str__',
        'payment_method',
        'total_price',
        'status'
    )




@admin.register(OrderitemModel)
class OrderitemAdmin(ModelAdmin):
    list_display = (
        "id",
        'book',
        'price'
    )
    
    def order(self, obj):
        return obj.order.user.first_name
    
    def book(self, obj):
        return obj.book.name
