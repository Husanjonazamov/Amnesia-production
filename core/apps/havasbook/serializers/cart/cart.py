from rest_framework import serializers
from core.apps.havasbook.serializers.cart.cartItem import CreateCartitemSerializer
from ...models import CartModel, CartitemModel
from decimal import Decimal
from django.db.models import Sum
from django_core.serializers import AbstractTranslatedSerializer
from core.apps.havasbook.serializers.book.currency import BaseCurrencyPriceMixin





class BaseCartSerializer(BaseCurrencyPriceMixin, serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = CartModel
        fields = [
            'id',
            'user',
            'total_price'
        ]
        
    def get_user(self, obj):
        from core.apps.accounts.serializers import UserSerializer
        return UserSerializer(obj.user).data

    def get_total_price(self, obj):
        return self.get_currency_price(obj.total_price)

    

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        for field in ["total_price"]:
            value = rep.get(field)
            if value is not None:
                value = Decimal(value).quantize(Decimal('0')) 
                rep[field] = int(value) 

        return rep




class ListCartSerializer(BaseCurrencyPriceMixin, serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    total_quantity = serializers.SerializerMethodField()
    total_discounted_price = serializers.SerializerMethodField()

    class Meta:
        model = CartModel
        fields = [
            'total_price',
            'total_quantity',
            'total_discounted_price',
            'products'
        ]

    def get_products(self, obj):
        from core.apps.havasbook.serializers.cart import ListCartitemSerializer
        items = obj.cart_items.all()
        return ListCartitemSerializer(items, many=True, context={'request': self.context.get('request')}).data

    def get_total_quantity(self, obj):
        return sum([item.quantity for item in obj.cart_items.all()])

    def get_total_price(self, obj):
        total = sum([item.book.price * item.quantity for item in obj.cart_items.all()])
        return self.get_currency_price(total)

    def get_total_discounted_price(self, obj):
        total = Decimal('0.00')
        for item in obj.cart_items.all():
            discount = item.book.discount_percent or 0
            discounted_price = Decimal(item.book.price) * (1 - Decimal(discount) / 100)
            total += discounted_price * item.quantity
        return self.get_currency_price(total)





class RetrieveCartSerializer(BaseCartSerializer):
    class Meta(BaseCartSerializer.Meta): ...




class CreateCartSerializer(BaseCartSerializer):
    cart_items = CreateCartitemSerializer(many=True, required=True)

    class Meta(BaseCartSerializer.Meta):
        model = CartModel
        fields = BaseCartSerializer.Meta.fields + ['cart_items']

    def validate_cart_items(self, value):
        if not value:
            raise serializers.ValidationError("Cart items bo'sh bo'lishi mumkin emas.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user


        cart_items_data = validated_data.pop('cart_items')

        cart, created = CartModel.objects.get_or_create(user=user)

        total_price_sum = Decimal('0.00') 

        for item_data in cart_items_data:
            book = item_data.get('book')
            color = item_data.get('color')  
            size = item_data.get('size')   
            quantity = 1  

            if not book:
                raise serializers.ValidationError("Item uchun book kiritilishi kerak.")

            total_price = Decimal(book.price) * Decimal(quantity)  
            total_price_sum += total_price

            existing_item = CartitemModel.objects.filter(
                cart=cart,
                book=book,
                color=color,
                size=size
            ).first()

            if existing_item:
                existing_item.quantity += 1
                existing_item.total_price = existing_item.book.price * existing_item.quantity
                existing_item.save()
            else:
                CartitemModel.objects.create(
                    cart=cart,
                    book=book,
                    color=color,  
                    size=size,    
                    quantity=quantity,  
                    total_price=total_price,
                )

        cart.total_price = Decimal(cart.total_price) + total_price_sum
        cart.save()

        return cart
