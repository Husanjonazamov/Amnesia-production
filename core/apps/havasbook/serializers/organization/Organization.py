from rest_framework import serializers

from core.apps.havasbook.models import OrganizationModel


class BaseOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationModel
        fields = [
            "id",
            "name",
        ]


class ListOrganizationSerializer(BaseOrganizationSerializer):
    class Meta(BaseOrganizationSerializer.Meta): ...


class RetrieveOrganizationSerializer(BaseOrganizationSerializer):
    class Meta(BaseOrganizationSerializer.Meta): ...


class CreateOrganizationSerializer(BaseOrganizationSerializer):
    class Meta(BaseOrganizationSerializer.Meta):
        fields = [
            "id",
            "name",
        ]
