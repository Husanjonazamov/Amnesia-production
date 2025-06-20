from rest_framework import serializers

from ...models import CategoryModel
from core.apps.havasbook.serializers.book.book import BaseBookSerializer
from django_core.serializers import AbstractTranslatedSerializer

class BaseCategorySerializer(AbstractTranslatedSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = CategoryModel
        translated_fields = [
            'name'
        ]
        fields = [
            'id',
            'name',
            'image',
        ]
        
    def get_image(self, obj):
        request = self.context.get("request")
        if request and obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None


class ListCategorySerializer(BaseCategorySerializer):
    class Meta(BaseCategorySerializer.Meta): ...


class RetrieveCategorySerializer(BaseCategorySerializer):
    books = BaseBookSerializer(many=True, read_only=True)
    class Meta(BaseCategorySerializer.Meta): 
        fields = BaseCategorySerializer.Meta.fields + ['books']


class CreateCategorySerializer(BaseCategorySerializer):
    class Meta(BaseCategorySerializer.Meta): ...
