from rest_framework import serializers

from ...models import OrderitemModel


class BaseOrderitemSerializer(serializers.ModelSerializer):
    order = serializers.SerializerMethodField()
    book = serializers.SerializerMethodField()
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
        return ListOrderSerializer(obj.order).data
    
    def get_book(self, obj):
        from core.apps.havasbook.serializers.book import ListBookSerializer
        return ListBookSerializer(obj.book).data
    


class ListOrderitemSerializer(BaseOrderitemSerializer):
    class Meta(BaseOrderitemSerializer.Meta): ...


class RetrieveOrderitemSerializer(BaseOrderitemSerializer):
    class Meta(BaseOrderitemSerializer.Meta): ...


class CreateOrderitemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderitemModel
        fields = [
            'book',
            'quantity',
        ]


class OrderItemSerializers(serializers.ModelSerializer):
    book = serializers.SerializerMethodField()
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
        return ListBookSerializer(obj.book).data
    
    
class ListOrderItemSerializers(serializers.ModelSerializer):
    book = serializers.SerializerMethodField()
    class Meta:
        model = OrderitemModel
        fields = [
            'id',
            'book',
            'quantity',
            'price'
        ]


    def get_book(self, obj):
        request = self.context.get('request')  
        book = obj.book
        image_url = book.image.url if book.image else None
        if image_url and request:
            image_url = request.build_absolute_uri(image_url)  

        return {
            "name": book.name,
            "price": book.price,
            "image": image_url,
            "color": book.color.first().title if book.color.exists() else None,
            "size": book.size.first().title if book.size.exists() else None
        }
