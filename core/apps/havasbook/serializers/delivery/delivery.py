from rest_framework import serializers

from ...models import DeliveryModel
from django_core.serializers import AbstractTranslatedSerializer

class BaseDeliverySerializer(AbstractTranslatedSerializer):
    class Meta:
        model = DeliveryModel
        translated_fields = [
            'title'
        ]
        fields = [
            'id',
            'title',
            'price'
        ]


class ListDeliverySerializer(BaseDeliverySerializer):
    class Meta(BaseDeliverySerializer.Meta): ...


class RetrieveDeliverySerializer(BaseDeliverySerializer):
    class Meta(BaseDeliverySerializer.Meta): ...


class CreateDeliverySerializer(BaseDeliverySerializer):
    class Meta(BaseDeliverySerializer.Meta): ...
