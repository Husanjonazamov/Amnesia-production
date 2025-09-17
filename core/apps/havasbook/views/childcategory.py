from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from core.apps.havasbook.models import ChildcategoryModel
from core.apps.havasbook.serializers.childcategory import (
    CreateChildcategorySerializer,
    ListChildcategorySerializer,
    RetrieveChildcategorySerializer,
)


@extend_schema(tags=["ChildCategory"])
class ChildcategoryView(BaseViewSetMixin, ReadOnlyModelViewSet):
    queryset = ChildcategoryModel.objects.all()
    serializer_class = ListChildcategorySerializer
    permission_classes = [AllowAny]

    action_permission_classes = {}
    action_serializer_class = {
        "list": ListChildcategorySerializer,
        "retrieve": RetrieveChildcategorySerializer,
        "create": CreateChildcategorySerializer,
    }
