from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from core.apps.havasbook.models import BrandModel
from core.apps.havasbook.serializers.brand import CreateBrandSerializer, ListBrandSerializer, RetrieveBrandSerializer


@extend_schema(tags=["brand"])
class BrandView(BaseViewSetMixin, ModelViewSet):
    queryset = BrandModel.objects.all()
    serializer_class = ListBrandSerializer
    permission_classes = [AllowAny]

    action_permission_classes = {}
    action_serializer_class = {
        "list": ListBrandSerializer,
        "retrieve": RetrieveBrandSerializer,
        "create": CreateBrandSerializer,
    }
