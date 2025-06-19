from rest_framework import serializers

from core.apps.havasbook.models import BrandModel


class BaseBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandModel
        fields = [
            "id",
            "name",
            "gender",
            
        ]


class ListBrandSerializer(BaseBrandSerializer):
    class Meta(BaseBrandSerializer.Meta): ...


class RetrieveBrandSerializer(BaseBrandSerializer):
    class Meta(BaseBrandSerializer.Meta): ...


class CreateBrandSerializer(BaseBrandSerializer):
    class Meta(BaseBrandSerializer.Meta):
        fields = [
            "id",
            "name",
            "gender",
        ]
