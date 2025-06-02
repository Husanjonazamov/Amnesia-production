from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from core.apps.havasbook.models import OrganizationModel
from core.apps.havasbook.serializers.organization import (
    CreateOrganizationSerializer,
    ListOrganizationSerializer,
    RetrieveOrganizationSerializer,
)


@extend_schema(tags=["Organization"])
class OrganizationView(BaseViewSetMixin, ReadOnlyModelViewSet):
    queryset = OrganizationModel.objects.all()
    serializer_class = ListOrganizationSerializer
    permission_classes = [AllowAny]

    action_permission_classes = {}
    action_serializer_class = {
        "list": ListOrganizationSerializer,
        "retrieve": RetrieveOrganizationSerializer,
        "create": CreateOrganizationSerializer,
    }
