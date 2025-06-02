from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from core.apps.accounts.models.user import User
from ..serializers.user import CreateUserSerializer, ListUserSerializer, RetrieveUserSerializer
from ..permissions import UserPermission  # siz yozgan permission

from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError



class UserView(BaseViewSetMixin, ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ListUserSerializer
    permission_classes = [AllowAny, UserPermission]
    action_permission_classes = {}

    action_serializer_class = {
        "list": ListUserSerializer,
        "retrieve": RetrieveUserSerializer,
        "create": CreateUserSerializer,
        "partial_update": CreateUserSerializer,
    }

   
