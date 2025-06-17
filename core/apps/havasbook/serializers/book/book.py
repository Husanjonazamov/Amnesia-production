import requests
from decimal import Decimal
from django.conf import settings
from rest_framework import serializers
from ...models import BookModel
from core.apps.havasbook.models.cart import CartitemModel, CartModel
from django_core.serializers import AbstractTranslatedSerializer
from config.env import env

class BaseBookSerializer(AbstractTranslatedSerializer):
    color = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    original_price = serializers.SerializerMethodField()

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
            'created_at',
        ]

    def get_color(self, obj):
        from core.apps.havasbook.serializers.variants import BaseColorSerializer
        request = self.context.get('request')
        return BaseColorSerializer(obj.color.all(), many=True, context={'request': request}).data

    def get_size(self, obj):
        from core.apps.havasbook.serializers import ListSizeSerializer
        return ListSizeSerializer(obj.size, many=True).data

    def convert_currency(self, amount: Decimal, to_currency: str) -> Decimal:
        if to_currency == "USD":
            return amount  # USD dan boshqa valyutaga aylantirish kerak emas

        url = env.str("EXCHANGE_URL")
        try:
            response = requests.get(url, timeout=3)
            data = response.json()
            rates = data.get("conversion_rates", {})
            rate = Decimal(rates.get(to_currency, 1))
            return round(amount * rate, 2)
        except Exception as e:
            print("Currency conversion failed:", e)
            return amount

    def get_price(self, obj):
        request = self.context.get("request")
        currency = request.query_params.get("currency", "USD").upper()

        amount = obj.price
        return self.convert_currency(Decimal(amount), currency)

    def get_original_price(self, obj):
        request = self.context.get("request")
        currency = request.query_params.get("currency", "USD").upper()

        amount = obj.original_price
        return self.convert_currency(Decimal(amount), currency)

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
