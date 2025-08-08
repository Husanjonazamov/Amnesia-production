from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from ..models import ProductsimageModel, ProductsModel
from ..serializers.products import (
    CreateProductsimageSerializer,
    CreateProductsSerializer,
    ListProductsimageSerializer,
    ListProductsSerializer,
    RetrieveProductsimageSerializer,
    RetrieveProductsSerializer,
)

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from core.apps.havasbook.filters.products import ProductsFilter



from pyinstrument import Profiler

@extend_schema(tags=["products"])
class ProductsView(BaseViewSetMixin, ReadOnlyModelViewSet):
    queryset = ProductsModel.objects.all()
    serializer_class = ListProductsSerializer
    permission_classes = [AllowAny]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ProductsFilter

    action_permission_classes = {}
    action_serializer_class = {
        "list": ListProductsSerializer,
        "retrieve": RetrieveProductsSerializer,
        "create": CreateProductsSerializer,
    }

    def list(self, request, *args, **kwargs):
        profiler = Profiler()
        profiler.start()

        response = super().list(request, *args, **kwargs)

        profiler.stop()
        print(profiler.output_text(unicode=True, color=True))

        return response



@extend_schema(tags=["productsImage"])
class ProductsimageView(BaseViewSetMixin, ReadOnlyModelViewSet):
    queryset = ProductsimageModel.objects.all()
    serializer_class = ListProductsimageSerializer
    permission_classes = [AllowAny]

    action_permission_classes = {}
    action_serializer_class = {
        "list": ListProductsimageSerializer,
        "retrieve": RetrieveProductsimageSerializer,
        "create": CreateProductsimageSerializer,
    }
