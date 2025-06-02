from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from ..models import DeliveryModel
from ..serializers.delivery import CreateDeliverySerializer, ListDeliverySerializer, RetrieveDeliverySerializer


@extend_schema(tags=["delivery"])
class DeliveryView(BaseViewSetMixin, ReadOnlyModelViewSet):
    queryset = DeliveryModel.objects.all()
    serializer_class = ListDeliverySerializer
    permission_classes = [AllowAny]

    action_permission_classes = {}
    action_serializer_class = {
        "list": ListDeliverySerializer,
        "retrieve": RetrieveDeliverySerializer,
        "create": CreateDeliverySerializer,
    }
