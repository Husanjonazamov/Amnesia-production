from rest_framework import serializers

from core.apps.havasbook.models import GenderModel


class BaseGenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenderModel
        fields = [
            "id",
            "gender",
        ]


class ListGenderSerializer(BaseGenderSerializer):
    class Meta(BaseGenderSerializer.Meta): ...


class RetrieveGenderSerializer(BaseGenderSerializer):
    class Meta(BaseGenderSerializer.Meta): ...


class CreateGenderSerializer(BaseGenderSerializer):
    class Meta(BaseGenderSerializer.Meta):
        fields = [
            "id",
            "gender",
        ]
