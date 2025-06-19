from rest_framework import serializers

from core.apps.havasbook.models import SubcategoryModel


class BaseSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubcategoryModel
        fields = [
            "id",
            "name",
            "category"
        ]


class ListSubcategorySerializer(BaseSubcategorySerializer):
    class Meta(BaseSubcategorySerializer.Meta): ...


class RetrieveSubcategorySerializer(BaseSubcategorySerializer):
    class Meta(BaseSubcategorySerializer.Meta): ...


class CreateSubcategorySerializer(BaseSubcategorySerializer):
    class Meta(BaseSubcategorySerializer.Meta):
        fields = [
            "id",
            "name",
            "category"
        ]
