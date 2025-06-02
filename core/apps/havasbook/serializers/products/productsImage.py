from rest_framework import serializers

from ...models import ProductsimageModel


class BaseProductsimageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsimageModel
        exclude = [
            "created_at",
            "updated_at",
        ]


class ListProductsimageSerializer(BaseProductsimageSerializer):
    class Meta(BaseProductsimageSerializer.Meta): ...


class RetrieveProductsimageSerializer(BaseProductsimageSerializer):
    class Meta(BaseProductsimageSerializer.Meta): ...


class CreateProductsimageSerializer(BaseProductsimageSerializer):
    class Meta(BaseProductsimageSerializer.Meta): ...
