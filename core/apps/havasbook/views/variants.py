from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from ..models import ColorModel, SizeModel
from ..serializers.variants import (
    CreateColorSerializer,
    CreateSizeSerializer,
    ListColorSerializer,
    ListSizeSerializer,
    RetrieveColorSerializer,
    RetrieveSizeSerializer,
)




@extend_schema(tags=["color"])
class ColorView(BaseViewSetMixin, ReadOnlyModelViewSet):
    queryset = ColorModel.objects.all()
    serializer_class = ListColorSerializer
    permission_classes = [AllowAny]

    action_permission_classes = {}
    action_serializer_class = {
        "list": ListColorSerializer,
        "retrieve": RetrieveColorSerializer,
        "create": CreateColorSerializer,
    }


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context




@extend_schema(tags=["size"])
class SizeView(BaseViewSetMixin, ReadOnlyModelViewSet):
    queryset = SizeModel.objects.all()
    serializer_class = ListSizeSerializer
    permission_classes = [AllowAny]

    action_permission_classes = {}
    action_serializer_class = {
        "list": ListSizeSerializer,
        "retrieve": RetrieveSizeSerializer,
        "create": CreateSizeSerializer,
    }
