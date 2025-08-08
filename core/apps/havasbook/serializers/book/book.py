import requests
from decimal import Decimal
from django.conf import settings
from rest_framework import serializers
from ...models import BookModel
from core.apps.havasbook.models.cart import CartitemModel, CartModel
from django_core.serializers import AbstractTranslatedSerializer
from core.apps.havasbook.models.book import CurrencyChoices
from core.apps.havasbook.serializers.book.currency import BaseCurrencyPriceMixin
from core.apps.havasbook.serializers.book.BookService import ProductServices as PS


class BaseBookSerializer(AbstractTranslatedSerializer):
    color = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    # price = serializers.SerializerMethodField()
    # original_price = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = BookModel
        translated_fields = [
            "name",
            "description"
        ]
        fields = [
            'id',
            'category',
            'name',
            'image',
            'color',
            'size',
            'original_price',
            'discount_percent',
            'price',
            'quantity',
            "book_id",
            'sold_count',
            'view_count',
            'is_discount',
            'popular',
            'is_preorder',
            'gender',
            "brand",
            'created_at',
        ]
        
    def get_gender(self, obj):
        return PS.get_gender(obj.gender)
    
    def get_brand(self, obj):
        return PS.get_brand(obj.brand)
    

    def get_color(self, obj):
        return PS.get_colors(obj.color.all(), self.context.get("request"))

    def get_size(self, obj):
        return PS.get_sizes(obj.size.all())
        

    def get_image(self, obj):
        return PS.get_image_url(obj.image, self.context.get("request"))


    # def get_price(self, obj):
    #     return self.get_currency_price(obj.price or 0)
    
    
    # def get_original_price(self, obj):
    #     return self.get_currency_price(obj.original_price or 0)
    



class ListBookSerializer(BaseBookSerializer):
    class Meta(BaseBookSerializer.Meta):
        pass


class RetrieveBookSerializer(BaseBookSerializer):
    cart_id = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta(BaseBookSerializer.Meta):
        fields = BaseBookSerializer.Meta.fields + [
            'cart_id',
            'description',
            'images',
        ]

    def get_cart_id(self, obj):
        request = self.context.get('request')
        cart = CartModel.objects.filter(user=request.user).first()
        if cart:
            cart_item = CartitemModel.objects.filter(cart=cart, book=obj).first()
            if cart_item:
                return cart.id
        return None
    

    def get_images(self, obj):
        from core.apps.havasbook.serializers.book import ListBookimageSerializer
        request = self.context.get('request')
        return ListBookimageSerializer(obj.images.all(), many=True, context={'request': request}).data



class CreateBookSerializer(BaseBookSerializer):
    class Meta(BaseBookSerializer.Meta):
        pass
