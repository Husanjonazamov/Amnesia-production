from rest_framework import serializers

from ...models import ProductsModel


class BaseProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsModel
        exclude = [
            "created_at",
            "updated_at",
        ]


class ListProductsSerializer(BaseProductsSerializer):
    class Meta(BaseProductsSerializer.Meta): ...


class RetrieveProductsSerializer(BaseProductsSerializer):
    class Meta(BaseProductsSerializer.Meta): ...


class CreateProductsSerializer(BaseProductsSerializer):
    class Meta(BaseProductsSerializer.Meta): ...
