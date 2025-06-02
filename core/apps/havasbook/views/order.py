from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from ..models import OrderitemModel, OrderModel, OrderStatus
from ..serializers.order import (
    CreateOrderitemSerializer,
    CreateOrderSerializer,
    ListOrderitemSerializer,
    ListOrderSerializer,
    RetrieveOrderitemSerializer,
    RetrieveOrderSerializer,
    OrderStatusSerializers
)
from django_core.paginations import CustomPagination
from rest_framework.decorators import action
from core.apps.havasbook.filters.order import OrderFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..serializers.order.cencel_order import send_cancel_order
from rest_framework import status
from core.apps.user.permissions.user import UserPermission




@extend_schema(tags=["order"])
class OrderView(BaseViewSetMixin, ModelViewSet):
    queryset = OrderModel.objects.all()
    serializer_class = ListOrderSerializer
    permission_classes = [AllowAny, UserPermission]
    filterset_class = OrderFilter
    pagination_class = CustomPagination

    filter_backends = [DjangoFilterBackend]  # ✅ SHART

    action_permission_classes = {}
    action_serializer_class = {
        "list": ListOrderSerializer,
        "retrieve": RetrieveOrderSerializer,
        "create": CreateOrderSerializer,
    }
    
    
    @action(detail=False, methods=["get"], url_path="me", permission_classes=[AllowAny, UserPermission])
    def me(self, request):
        user = request.user
        queryset = self.filter_queryset(self.get_queryset().filter(user=user))
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": True, "data": serializer.data})
    

    @action(detail=True, methods=["patch"], url_path="cancel", permission_classes=[AllowAny, UserPermission])
    def cancel_order(self, request, pk=None):
        try:
            order = self.get_object()

            if order.user != request.user:
                return Response({"detail": "You are not allowed to cancel this order."}, status=status.HTTP_403_FORBIDDEN)

            if order.status == OrderStatus.CANCELLED:
                return Response({"detail": "Order is already cancelled."}, status=status.HTTP_400_BAD_REQUEST)

            serializer = OrderStatusSerializers(order, data={"status": OrderStatus.CANCELLED}, partial=True)
            if serializer.is_valid():
                serializer.save()

                send_cancel_order(order)

                return Response({"status": True, "data": {"message": "Order successfully cancelled."}}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except OrderModel.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        



@extend_schema(tags=["orderITem"])
class OrderitemView(BaseViewSetMixin, ModelViewSet):
    queryset = OrderitemModel.objects.all()
    serializer_class = ListOrderitemSerializer
    permission_classes = [AllowAny, UserPermission]

    action_permission_classes = {}
    action_serializer_class = {
        "list": ListOrderitemSerializer,
        "retrieve": RetrieveOrderitemSerializer,
        "create": CreateOrderitemSerializer,
    }
