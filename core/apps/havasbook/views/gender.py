from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from core.apps.havasbook.models import GenderModel
from core.apps.havasbook.serializers.gender import (
    CreateGenderSerializer,
    ListGenderSerializer,
    RetrieveGenderSerializer,
)


@extend_schema(tags=["gender"])
class GenderView(BaseViewSetMixin, ReadOnlyModelViewSet):
    queryset = GenderModel.objects.all()
    serializer_class = ListGenderSerializer
    permission_classes = [AllowAny]

    action_permission_classes = {}
    action_serializer_class = {
        "list": ListGenderSerializer,
        "retrieve": RetrieveGenderSerializer,
        "create": CreateGenderSerializer,
    }
