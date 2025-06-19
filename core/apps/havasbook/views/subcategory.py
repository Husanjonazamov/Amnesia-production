from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from core.apps.havasbook.models import SubcategoryModel
from core.apps.havasbook.serializers.subcategory import (
    CreateSubcategorySerializer,
    ListSubcategorySerializer,
    RetrieveSubcategorySerializer,
)


@extend_schema(tags=["subcategory"])
class SubcategoryView(BaseViewSetMixin, ReadOnlyModelViewSet):
    queryset = SubcategoryModel.objects.all()
    serializer_class = ListSubcategorySerializer
    permission_classes = [AllowAny]

    action_permission_classes = {}
    action_serializer_class = {
        "list": ListSubcategorySerializer,
        "retrieve": RetrieveSubcategorySerializer,
        "create": CreateSubcategorySerializer,
    }
