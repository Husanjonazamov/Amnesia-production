from rest_framework import serializers

from ...models import PreorderModel
from core.apps.havasbook.models.book import BookModel
from core.apps.havasbook.serializers.book import BaseBookSerializer

from core.apps.havasbook.models import ColorModel, SizeModel
from .send_preorder import send_preorder_to_telegram, send_user_order
from core.apps.havasbook.models import DeliveryModel, LocationModel
from core.apps.havasbook.models.preorder import OrderStatus
from core.apps.havasbook.serializers.location import CreateLocationSerializer


class BasePreorderSerializer(serializers.ModelSerializer):
    book = serializers.SerializerMethodField()

    class Meta:
        model = PreorderModel
        fields = [
            "id",
            "book",
            "created_at",
            "reciever_name",
            "reciever_phone",
            "count",
            "status",
            "total_price"
        ]

    def get_book(self, obj):
        book = obj.book
        request = self.context.get('request') 

        image_url = book.image.url if book.image else None
        if image_url and request:
            image_url = request.build_absolute_uri(image_url)

        return {
            "id": book.id,  
            "name": book.name,  # type: str
            "image": image_url,  # type: str
            "color": obj.color.name if obj.color else None,  # type: str | None
            "size": obj.size.name if obj.size else None,  # type: str | None
            "price": str(book.price),  # type: str
            "original_price": str(book.original_price),  # type: str
            "discount_percent": str(book.discount_percent),  # type: str
            "description": book.description,  # type: str
        }


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Fields with the correct types as str
        representation["created_at"] = str(instance.created_at)  
        representation["reciever_name"] = str(instance.reciever_name)  
        representation["reciever_phone"] = str(instance.reciever_phone)  
        representation["count"] = str(instance.count)  
        representation["status"] = str(instance.status)  
        representation["total_price"] = str(instance.total_price) 
        
        return representation

class ListPreorderSerializer(BasePreorderSerializer):
    class Meta(BasePreorderSerializer.Meta): ...


class RetrievePreorderSerializer(BasePreorderSerializer):
    class Meta(BasePreorderSerializer.Meta): ...




class CreatePreorderSerializer(serializers.ModelSerializer):
    location = CreateLocationSerializer()
    delivery_method = serializers.PrimaryKeyRelatedField(queryset=DeliveryModel.objects.all())
    reciever = serializers.DictField(write_only=True)  # {'name': ..., 'phone': ...}
    book = serializers.PrimaryKeyRelatedField(queryset=BookModel.objects.all())
    color = serializers.PrimaryKeyRelatedField(queryset=ColorModel.objects.all(), required=False, allow_null=True)
    size = serializers.PrimaryKeyRelatedField(queryset=SizeModel.objects.all(), required=False, allow_null=True)
    count = serializers.IntegerField()

    class Meta:
        model = PreorderModel
        fields = [
            'location',
            'delivery_method',
            'reciever',
            'book',
            'color',
            'size',
            'count',
            'payment_method',
        ]

    def create(self, validated_data):
        location_data = validated_data.pop('location')
        reciever_data = validated_data.pop('reciever')
        book = validated_data.pop('book')
        color = validated_data.pop('color', None)
        size = validated_data.pop('size', None)
        count = validated_data.pop('count')
        delivery_method = validated_data.pop('delivery_method')
        payment_method = validated_data.pop('payment_method', None)

        user = self.context['request'].user

        location = LocationModel.objects.create(**location_data)

        # Umumiy narx hisoblash (kitob narxi * soni)
        book_price = book.price
        total_price = book_price * count

        preorder = PreorderModel.objects.create(
            user=user,
            location=location,
            delivery_method=delivery_method,
            payment_method=payment_method,
            reciever_name=reciever_data['name'],
            reciever_phone=reciever_data['phone'],
            book=book,
            color=color,
            size=size,
            count=count,
            total_price=total_price,
        )

        # Telegram va foydalanuvchiga xabar yuborish
        send_preorder_to_telegram(
            preorder=preorder,
            location_name=location.title,
            latitude=location.lat,
            longitude=location.long, 
            request=self.context['request']
        )
        send_user_order(preorder)

        return preorder
    
    
class OrderStatusSerializers(serializers.ModelSerializer):
    class Meta:
        model = PreorderModel
        fields = [
            'status'
        ]

    def validate_status(self, value):
        valid_statuses = [status.value for status in OrderStatus]
        if value not in valid_statuses:
            raise serializers.ValidationError("Invalid status.")
        return value