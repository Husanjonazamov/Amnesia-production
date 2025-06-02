from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ..models import LocationModel
from ..serializers.location import CreateLocationSerializer, ListLocationSerializer, RetrieveLocationSerializer


from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404




@extend_schema(tags=["location"])
class LocationView(BaseViewSetMixin, ModelViewSet):
    queryset = LocationModel.objects.all()
    serializer_class = ListLocationSerializer
    permission_classes = [IsAuthenticated]

    action_permission_classes = {}
    action_serializer_class = {
        "list": ListLocationSerializer,
        "retrieve": RetrieveLocationSerializer,
        "create": CreateLocationSerializer,
    }
    
    
    def destroy(self, request, pk=None):
        self.permission_classes = [IsAuthenticated]
        
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        
        location = get_object_or_404(LocationModel, pk=pk, user=request.user)
        
        location.delete()

        return Response({
            'status': True
        }, status=status.HTTP_200_OK)
