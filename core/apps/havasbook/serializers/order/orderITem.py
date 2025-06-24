from rest_framework import serializers
from decimal import Decimal
from ...models import OrderitemModel
from core.apps.havasbook.serializers.book.currency import BaseCurrencyPriceMixin


class BaseOrderitemSerializer(BaseCurrencyPriceMixin, serializers.ModelSerializer):
    order = serializers.SerializerMethodField()
    book = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = OrderitemModel
        fields = [
            'id',
            'order',
            'book',
            'quantity',
            'price'
        ]

    def get_order(self, obj): 
        from core.apps.havasbook.serializers.order import ListOrderSerializer
        return ListOrderSerializer(obj.order, context=self.context).data

    def get_book(self, obj):
        from core.apps.havasbook.serializers.book import ListBookSerializer
        return ListBookSerializer(obj.book, context=self.context).data

    def get_price(self, obj):
        return self.get_currency_price(obj.price)


class ListOrderitemSerializer(BaseOrderitemSerializer):
    class Meta(BaseOrderitemSerializer.Meta):
        pass


class RetrieveOrderitemSerializer(BaseOrderitemSerializer):
    class Meta(BaseOrderitemSerializer.Meta):
        pass


class CreateOrderitemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderitemModel
        fields = [
            'book',
            'quantity',
        ]


class OrderItemSerializers(BaseCurrencyPriceMixin, serializers.ModelSerializer):
    book = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = OrderitemModel
        fields = [
            'id',
            'book',
            'quantity',
            'price'
        ]

    def get_book(self, obj):
        from core.apps.havasbook.serializers.book.book import ListBookSerializer
        return ListBookSerializer(obj.book, context=self.context).data

    def get_price(self, obj):
        return self.get_currency_price(obj.price)


class ListOrderItemSerializers(BaseCurrencyPriceMixin, serializers.ModelSerializer):
    book = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = OrderitemModel
        fields = [
            'id',
            'book',
            'quantity',
            'price'
        ]

    def get_price(self, obj):
        return self.get_currency_price(obj.price)

    def get_book(self, obj):
        request = self.context.get('request')
        book = obj.book
        image_url = book.image.url if book.image else None

        if image_url and request:
            image_url = request.build_absolute_uri(image_url)

        return {
            "name": book.name,
            "price": self.get_currency_price(book.price),
            "image": image_url,
            "color": book.color.first().title if book.color.exists() else None,
            "size": book.size.first().title if book.size.exists() else None
        }
