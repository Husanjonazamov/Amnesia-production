from rest_framework import serializers

from ...models import BookimageModel


class BaseBookimageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = BookimageModel
        fields = [
            'id',
            'image'
        ]


    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            image_url = obj.image.url
            if request:
                return request.build_absolute_uri(image_url)
            return image_url
        return None

class ListBookimageSerializer(BaseBookimageSerializer):
    class Meta(BaseBookimageSerializer.Meta): ...


class RetrieveBookimageSerializer(BaseBookimageSerializer):
    class Meta(BaseBookimageSerializer.Meta): ...


class CreateBookimageSerializer(BaseBookimageSerializer):
    class Meta(BaseBookimageSerializer.Meta): ...
