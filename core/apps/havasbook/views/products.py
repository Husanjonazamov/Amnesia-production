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


@extend_schema(tags=["products"])
class ProductsView(BaseViewSetMixin, ReadOnlyModelViewSet):
    queryset = ProductsModel.objects.all()
    serializer_class = ListProductsSerializer
    permission_classes = [AllowAny]

    action_permission_classes = {}
    action_serializer_class = {
        "list": ListProductsSerializer,
        "retrieve": RetrieveProductsSerializer,
        "create": CreateProductsSerializer,
    }


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
