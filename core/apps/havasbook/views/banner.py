from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from ..models import BannerModel
from ..serializers.banner import (
    CreateBannerSerializer,
    ListBannerSerializer,
    RetrieveBannerSerializer,
)


@extend_schema(tags=["banner"])
class BannerView(BaseViewSetMixin, ReadOnlyModelViewSet):
    queryset = BannerModel.objects.all()
    serializer_class = ListBannerSerializer
    permission_classes = [AllowAny]

    action_permission_classes = {}
    action_serializer_class = {
        "list": ListBannerSerializer,
        "retrieve": RetrieveBannerSerializer,
        "create": CreateBannerSerializer,
    }

