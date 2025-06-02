from rest_framework import serializers

from ...models import ColorModel


from django.conf import settings



class BaseColorSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ColorModel
        fields = [
            'id',
            'image',
            'title',
            'name'
        ]


    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            image_url = obj.image.url
            if request:
                return request.build_absolute_uri(image_url)
            return image_url
        return None

   


class ListColorSerializer(BaseColorSerializer):
    class Meta(BaseColorSerializer.Meta): ...


class RetrieveColorSerializer(BaseColorSerializer):
    class Meta(BaseColorSerializer.Meta): ...


class CreateColorSerializer(BaseColorSerializer):
    class Meta(BaseColorSerializer.Meta): ...
