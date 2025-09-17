from rest_framework import serializers

from core.apps.havasbook.models import ChildcategoryModel


class BaseChildcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildcategoryModel
        fields = [
            "id",
            "name",
        ]


class ListChildcategorySerializer(BaseChildcategorySerializer):
    class Meta(BaseChildcategorySerializer.Meta): ...


class RetrieveChildcategorySerializer(BaseChildcategorySerializer):
    class Meta(BaseChildcategorySerializer.Meta): ...


class CreateChildcategorySerializer(BaseChildcategorySerializer):
    class Meta(BaseChildcategorySerializer.Meta):
        fields = [
            "id",
            "name",
        ]
