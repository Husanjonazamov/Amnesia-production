from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from django_core.paginations import CustomPagination

from ..models import BookimageModel, BookModel
from ..serializers.book import (
    CreateBookimageSerializer,
    CreateBookSerializer,
    ListBookimageSerializer,
    ListBookSerializer,
    RetrieveBookimageSerializer,
    RetrieveBookSerializer,
)

from django.db.models import Q
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from core.apps.havasbook.filters.book import BookFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from core.apps.havasbook.serializers import BaseBrandSerializer, BaseCategorySerializer, BaseSubcategorySerializer
from core.apps.havasbook.models import BrandModel, CategoryModel, SubcategoryModel



class BooksSearchView(ModelViewSet):
    serializer_class = ListBookSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = BookModel.objects.all()
        q = self.request.query_params.get('search', None)

        if q:
            queryset = queryset.filter(
                Q(name__icontains=q) | Q(description__icontains=q) 
            )
        return queryset




@extend_schema(tags=["book"])
class BookView(BaseViewSetMixin, ReadOnlyModelViewSet):
    queryset = BookModel.objects.all()
    serializer_class = ListBookSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = BookFilter
    ordering_fields = ['price', 'sold_count', 'view_count', 'created_at', 'popular'] 
    ordering = ['-sold_count'] 


    action_permission_classes = {}
    action_serializer_class = {
        "list": ListBookSerializer,
        "retrieve": RetrieveBookSerializer,
        "create": CreateBookSerializer,
    }
    

    def get_permissions(self):
        if self.action == 'retrieve':
            from core.apps.user.permissions.user import UserPermission
            return [UserPermission()]
        return [AllowAny()]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    


    @action(detail=False, methods=["get"], url_path="brands")
    def filter_by_gender_and_brand(self, request):
        gender = request.query_params.get("gender")
        brand_id = request.query_params.get("brand")

        if brand_id: 
            products = BookModel.objects.filter(
                brand_id=brand_id
            ).filter(
                Q(gender__gender=gender) | Q(gender__gender="unisex")
            )

            page = self.paginate_queryset(products)
            serializer = ListBookSerializer(page, many=True, context={"request": request})
            return self.get_paginated_response({
                "status": True,
                "results": serializer.data
            })

        brands = BrandModel.objects.filter(
            Q(gender__gender=gender) | Q(gender__gender='unisex')
        ).distinct()

        page = self.paginate_queryset(brands)
        serializer = BaseBrandSerializer(page, many=True, context=({"request": request}))
        return self.get_paginated_response(serializer.data)
    
    
    

    @action(detail=False, methods=["get"], url_path="category", permission_classes=[AllowAny])
    def filter_by_category(self, request):
        gender = request.query_params.get("gender")
        category_id = request.query_params.get("category")
        subcategory_id = request.query_params.get("subcategory")

        if subcategory_id:
            products = BookModel.objects.filter(
                subcategory_id=subcategory_id,
                subcategory__category__gender__gender__in=[gender, "unisex"]
            )
            page = self.paginate_queryset(products)
            serializer = ListBookSerializer(page, many=True, context={"request": request})
            return self.get_paginated_response({
                "status": True,
                "results": serializer.data
            })

        elif category_id:
            subcategories = SubcategoryModel.objects.filter(
                category_id=category_id,
                category__gender__gender__in=[gender, "unisex"]
            )
            page = self.paginate_queryset(subcategories)
            serializer = BaseSubcategorySerializer(page, many=True, context={"context": request})
            return self.get_paginated_response({
                "status": True,
                "results": serializer.data
            })
        elif gender:
            categories = CategoryModel.objects.filter(
                gender__gender__in=[gender, "unisex"]
            ).distinct()
            page = self.paginate_queryset(categories)
            serializer = BaseCategorySerializer(page, many=True, context={"request": request})
            return self.get_paginated_response({
                "status": True,
                "results": serializer.data
            })


        return Response({
            "status": False,
            "message": "Kamida gender yoki category yoki subcategory ID yuborilishi kerak."
        }, status=400)

        
        
    
    
    
@extend_schema(tags=["bookImage"])
class BookimageView(BaseViewSetMixin, ReadOnlyModelViewSet):
    queryset = BookimageModel.objects.all()
    serializer_class = ListBookimageSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    action_permission_classes = {}
    action_serializer_class = {
        "list": ListBookimageSerializer,
        "retrieve": RetrieveBookimageSerializer,
        "create": CreateBookimageSerializer,
    }


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
