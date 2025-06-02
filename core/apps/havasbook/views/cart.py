from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound



from ..models import CartitemModel, CartModel
from ..serializers.cart import (
    CreateCartitemSerializer,
    CreateCartSerializer,
    ListCartitemSerializer,
    ListCartSerializer,
    RetrieveCartitemSerializer,
    RetrieveCartSerializer,
)

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

from rest_framework.exceptions import ValidationError
from typing import Any
from core.apps.user.permissions.user import UserPermission


class CustomBaseViewSetMixin(object):
    action_serializer_class = {}
    action_permission_classes = {}

    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code >= 400:
            response.data = response.data  
        else:
            response.data = response.data  

        return super().finalize_response(request, response, *args, **kwargs)

    def get_serializer_class(self) -> Any:
        """
        Actionga mos serializer klassini olish.
        Agar maxsus serializer belgilanmagan bo'lsa, default serializer qaytadi.
        """
        return self.action_serializer_class.get(self.action, self.serializer_class)

    def get_permissions(self) -> Any:
        """
        Actionga mos permission klasslarini olish.
        Agar maxsus permission belgilanmagan bo'lsa, default permission qaytadi.
        """
        return [
            permission()
            for permission in self.action_permission_classes.get(
                self.action, self.permission_classes
            )
        ]





@extend_schema(tags=["cart"])
class CartView(CustomBaseViewSetMixin, ModelViewSet):
    queryset = CartModel.objects.all()
    serializer_class = ListCartSerializer
    permission_classes = [AllowAny, UserPermission]

    action_permission_classes = {}
    action_serializer_class = {
        "list": ListCartSerializer,
        "retrieve": RetrieveCartSerializer,
        "create": CreateCartSerializer,
    }

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user=request.user)
        if not queryset.exists():
            return Response({})

        cart = queryset.first()
        serializer = self.get_serializer(cart)
        return Response(serializer.data)
    
    def get_serializer_context(self):
            return {'request': self.request}

    


class CartitemView(BaseViewSetMixin, ReadOnlyModelViewSet):
    queryset = CartitemModel.objects.all()
    serializer_class = ListCartitemSerializer
    permission_classes = [AllowAny, UserPermission]

    action_permission_classes = {}
    action_serializer_class = {
        "list": ListCartitemSerializer,
        "retrieve": RetrieveCartitemSerializer,
        "create": CreateCartitemSerializer,
    }
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, pk=None):
        self.permission_classes = [UserPermission]
        
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        
        cart_item = get_object_or_404(CartitemModel, pk=pk, cart__user=request.user)

        cart = cart_item.cart
        cart.total_price -= cart_item.total_price  
        cart.save()  

        cart_item.delete()

        return Response({'status': True}, status=status.HTTP_200_OK)


    def patch(self, request, pk=None):
        self.permission_classes = [AllowAny, UserPermission]
    
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
            
        quantity = request.data.get("quantity")
        cart_item = get_object_or_404(CartitemModel, pk=pk, cart__user=request.user) 

        book = cart_item.book

        if quantity > book.quantity:
            raise ValidationError(
               f"Maxsulot miqdori ombordagi mavjud miqdordan ortiq bo'lishi mumkin emas."
            )

        
        new_total_price = cart_item.book.price * quantity  
        old_total_price = cart_item.total_price  


        if quantity == 0:
            cart = cart_item.cart
            cart.total_price -= cart_item.total_price
            cart.save()
            cart_item.delete()


            return Response(
                {"status": True, "message": "Mahsulot savatdan o'chirildi."},
                status=status.HTTP_200_OK
            )


        cart_item.quantity = quantity
        cart_item.total_price = new_total_price
        cart_item.save()

        cart = cart_item.cart

        cart.total_price += (new_total_price - old_total_price) 
        cart.save() 

        cart_item_serializer = ListCartitemSerializer(cart_item)
        cart_serializer = ListCartSerializer(cart)

        return Response(
            {
                "status": True,
                "message": "Quantity and total_price updated successfully",
                "data": {
                    "cart_item": cart_item_serializer.data,
                    "cart": cart_serializer.data
                }
            },
            status=status.HTTP_200_OK
        )



    @action(detail=False, methods=["delete"], url_path="clear")
    def clear_cart(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        cart_items = CartitemModel.objects.filter(cart__user=request.user)

        if not cart_items.exists():
            return Response(
                {"detail": "Savatchangizda mahsulotlar yo‘q"},
                status=status.HTTP_404_NOT_FOUND,
            )

        cart = cart_items.first().cart
        cart_items.delete()

        cart.total_price = 0
        cart.save()

        return Response(
            {"status": True, "message": "Savatchadagi barcha mahsulotlar tozalandi"}
            # status=status.HTTP_204_NO_CONTENT
        )