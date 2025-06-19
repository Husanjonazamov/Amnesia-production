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
        gender_slug = request.query_params.get("gender")
        brand_id = request.query_params.get("brand")

        if not gender_slug:
            return Response({"status": False, "error": "gender is required"}, status=400)

        if brand_id: 
            products = BookModel.objects.filter(
                brand_id=brand_id
            ).filter(
                Q(gender__gender=gender_slug) | Q(gender__gender="unisex")
            )

            page = self.paginate_queryset(products)
            serializer = ListBookSerializer(page, many=True, context={"request": request})
            return self.get_paginated_response({
                "status": True,
                "results": serializer.data
            })

        brands = BookModel.objects.filter(
            Q(gender__gender=gender_slug) | Q(gender__gender="unisex"),
            brand__isnull=False
        ).values("brand__id", "brand__name").distinct()

        brand_list = [{"id": b["brand__id"], "name": b["brand__name"]} for b in brands]

        page_size = 10
        page = int(request.query_params.get("page", 1))
        total_items = len(brand_list)
        total_pages = (total_items + page_size - 1) 
        start = (page - 1) * page_size
        end = start + page_size
        results = brand_list[start:end]

        data = {
            "status": True,
            "data": {
                "links": {
                    "previous": None if page == 1 else f"?page={page - 1}",
                    "next": None if page >= total_pages else f"?page={page + 1}"
                },
                "total_items": total_items,
                "total_pages": total_pages,
                "page_size": page_size,
                "current_page": page,
                "results": results
            }
        }
        return Response(data)

    
    
    
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
