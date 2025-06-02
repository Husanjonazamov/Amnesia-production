from rest_framework import serializers

from ...models import SizeModel


class BaseSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SizeModel
        fields = [
            'id',
            'title',
            'name'
        ]


class ListSizeSerializer(BaseSizeSerializer):
    class Meta(BaseSizeSerializer.Meta): ...


class RetrieveSizeSerializer(BaseSizeSerializer):
    class Meta(BaseSizeSerializer.Meta): ...


class CreateSizeSerializer(BaseSizeSerializer):
    class Meta(BaseSizeSerializer.Meta): ...
