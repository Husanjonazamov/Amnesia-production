import requests
from decimal import Decimal
from django.conf import settings
from rest_framework import serializers
from ...models import BookModel
from core.apps.havasbook.models.cart import CartitemModel, CartModel
from django_core.serializers import AbstractTranslatedSerializer
from core.apps.havasbook.models.book import CurrencyChoices
from core.apps.havasbook.serializers.book.currency import convert_currency



class BaseBookSerializer(AbstractTranslatedSerializer):
    color = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
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
        from core.apps.havasbook.serializers.gender import BaseGenderSerializer
        return BaseGenderSerializer(obj.gender).data
    
    def get_brand(self, obj):
        from core.apps.havasbook.serializers.brand import BaseBrandSerializer
        return BaseBrandSerializer(obj.brand).data
    

    def get_color(self, obj):
        from core.apps.havasbook.serializers.variants import BaseColorSerializer
        request = self.context.get('request')
        return BaseColorSerializer(obj.color.all(), many=True, context={'request': request}).data

    def get_size(self, obj):
        from core.apps.havasbook.serializers import ListSizeSerializer
        return ListSizeSerializer(obj.size, many=True).data

    def get_image(self, obj):
        request = self.context.get("request")
        if request and obj.image:
            return request.build_absolute_uri(obj.image.url)


    def get_price(self, obj):
        request = self.context.get("request")
        currency = request.query_params.get("currency", "USD").upper()

        if currency not in CurrencyChoices.values:
            currency = "USD"

        return convert_currency(obj.price or obj.original_price, currency)
    
    

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        for field in ["discount_percent", "price", "original_price"]:
            value = rep.get(field)
            if value is not None:
                value = Decimal(value)
                rep[field] = int(value) if value == int(value) else float(value)

        return rep


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
