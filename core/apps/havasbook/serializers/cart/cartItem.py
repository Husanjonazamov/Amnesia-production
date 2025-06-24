from rest_framework import serializers

from ...models import CartitemModel, CartModel
from core.apps.havasbook.models.book import BookModel
from core.apps.havasbook.models.variants import ColorModel, SizeModel
from core.apps.havasbook.serializers.book.currency import BaseCurrencyPriceMixin


class BaseCartitemSerializer(BaseCurrencyPriceMixin, serializers.ModelSerializer):
    book = serializers.SerializerMethodField() 
    cart = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    
    
    class Meta:
        model = CartitemModel
        fields = [
            'id',
            'cart',
            'book',
            'color',
            'size',
            'quantity',
            'total_price'
        ]

    def get_cart(self, obj):
        from core.apps.havasbook.serializers.cart.cart import ListCartSerializer
        return ListCartSerializer(obj.cart, context=self.context).data  

    def get_book(self, obj):
        from core.apps.havasbook.serializers.book import ListBookSerializer
        return ListBookSerializer(obj.book, context=self.context).data  


    def get_color(self, obj):
        if obj.color:
            from core.apps.havasbook.serializers.variants import ListColorSerializer
            return ListColorSerializer(obj.color).data
        return None

    def get_size(self, obj):
        if obj.size:
            from core.apps.havasbook.serializers.variants import ListSizeSerializer
            return ListSizeSerializer(obj.size).data
        return None




from decimal import Decimal
from rest_framework import serializers


class ListCartitemSerializer(BaseCurrencyPriceMixin, serializers.ModelSerializer):
    product_id = serializers.IntegerField(source="book.id")
    name = serializers.CharField(source='book.name')
    color = serializers.CharField(source='color.name', default=None)
    size = serializers.CharField(source='size.name', default=None)
    image = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    discounted_total_price = serializers.SerializerMethodField()
    discount_percent = serializers.SerializerMethodField()
    available_quantity = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartitemModel
        fields = [
            'id',
            'product_id',
            'name',
            'color',
            'size',
            'image',
            'price',
            'total_price',
            'discounted_total_price',
            'quantity',
            'discount_percent',
            'available_quantity'
        ]

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.book.image and request:
            return request.build_absolute_uri(obj.book.image.url)
        return None

    def get_price(self, obj):
        return self.get_currency_price(obj.book.price)

    def get_total_price(self, obj):
        return self.get_currency_price(obj.book.price * obj.quantity)

    def get_discounted_total_price(self, obj):
        price = Decimal(obj.book.price)
        discount = getattr(obj.book, 'discount_percent', 0) or 0
        discounted = price * (Decimal(1) - Decimal(discount) / 100)
        return self.get_currency_price(discounted * obj.quantity)

    def get_discount_percent(self, obj):
        return getattr(obj.book, 'discount_percent', 0)

    def get_available_quantity(self, obj):
        return obj.book.quantity




class RetrieveCartitemSerializer(BaseCartitemSerializer):
    class Meta(BaseCartitemSerializer.Meta): ...




class CreateCartitemSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=BookModel.objects.all(), write_only=True)  # product_id
    color = serializers.PrimaryKeyRelatedField(queryset=ColorModel.objects.all(), required=False, allow_null=True)
    size = serializers.PrimaryKeyRelatedField(queryset=SizeModel.objects.all(), required=False, allow_null=True)
    quantity = serializers.IntegerField(min_value=1, default=1)
    
    class Meta:
        model = CartitemModel
        fields = [
            'id',
            'book',
            'color',
            'size',
            'quantity',
            'total_price'
        ]

    def validate(self, attrs):
        book = attrs.get('book')
        quantity = attrs.get('quantity')

        total_price = book.price * quantity

        attrs['total_price'] = total_price
        return attrs

