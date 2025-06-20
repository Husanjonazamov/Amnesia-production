from rest_framework import serializers

from core.apps.havasbook.models import BrandModel


class BaseBrandSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = BrandModel
        fields = [
            "id",
            "name",
            "gender",
            "image"
            
        ]
        
    def get_image(self, obj):
        request = self.context.get("request")
        if request and obj.image:
            return request.build_absolute_uri(obj.image.url)
            


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
