from rest_framework import serializers

from ...models import LocationModel
from django_core.serializers import AbstractTranslatedSerializer


class BaseLocationSerializer(AbstractTranslatedSerializer):
    class Meta:
        model = LocationModel
        fields = [
            'id',
            'title',
            'user',
            'long',
            'lat'
        ]


class ListLocationSerializer(BaseLocationSerializer):
    class Meta(BaseLocationSerializer.Meta): ...


class RetrieveLocationSerializer(BaseLocationSerializer):
    class Meta(BaseLocationSerializer.Meta): ...



class CreateLocationSerializer(BaseLocationSerializer):
    class Meta(BaseLocationSerializer.Meta): 
        fields = [
            'id',
            'lat',
            'long',
            'title'
        ]

    def create(self, validated_data):
        user = self.context['request'].user  
        return LocationModel.objects.create(user=user, **validated_data)
