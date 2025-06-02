from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from ..models import PreorderModel
from ..serializers.preorder import CreatePreorderSerializer, ListPreorderSerializer, RetrievePreorderSerializer
from django_core.paginations import CustomPagination
from rest_framework.decorators import action
from core.apps.havasbook.filters.preorder import PreorderFilter
from django_filters.rest_framework import DjangoFilterBackend
from core.apps.user.permissions.user import UserPermission



@extend_schema(tags=["preorder"])
class PreorderView(BaseViewSetMixin, ModelViewSet):
    queryset = PreorderModel.objects.all()
    serializer_class = ListPreorderSerializer
    permission_classes = [AllowAny, UserPermission]
    filterset_class = PreorderFilter
    pagination_class = CustomPagination

    filter_backends = [DjangoFilterBackend] 

    action_permission_classes = {}
    action_serializer_class = {
        "list": ListPreorderSerializer,
        "retrieve": RetrievePreorderSerializer,
        "create": CreatePreorderSerializer,
    }


    @action(detail=False, methods=["get"], url_path="me", permission_classes=[AllowAny, UserPermission])
    def me(self, request):
        user = request.user
        queryset = self.filter_queryset(
            self.get_queryset().filter(user=user)
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": True, "data": serializer.data})
