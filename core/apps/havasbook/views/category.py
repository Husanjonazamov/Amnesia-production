from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet
from django_core.paginations import CustomPagination

from ..models import CategoryModel
from ..serializers.category import CreateCategorySerializer, ListCategorySerializer, RetrieveCategorySerializer


@extend_schema(tags=["category"])
class CategoryView(BaseViewSetMixin, ReadOnlyModelViewSet):
    queryset = CategoryModel.objects.all()
    serializer_class = ListCategorySerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    action_permission_classes = {}
    action_serializer_class = {
        "list": ListCategorySerializer,
        "retrieve": RetrieveCategorySerializer,
        "create": CreateCategorySerializer,
    }
