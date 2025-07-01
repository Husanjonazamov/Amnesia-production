# core/apps/havasbook/filters/helpers/book_helpers.py

from django.db.models import Q
from core.apps.havasbook.models import BookModel, BrandModel, CategoryModel, SubcategoryModel
from core.apps.havasbook.serializers import (
    BaseBrandSerializer, BaseCategorySerializer, BaseSubcategorySerializer, ListBookSerializer
)
from rest_framework.response import Response
import re






def parse_id_list(param):
    if not param:
        return []
    return list(map(int, re.findall(r'\d+', param)))





def get_filtered_brands(request, view):
    gender = request.query_params.get("gender")
    brand_param = request.query_params.get("brand")
    brand_ids = parse_id_list(brand_param)

    if brand_ids:
        products = BookModel.objects.filter(
            brand_id__in=brand_ids
        ).filter(
            Q(gender__gender=gender) | Q(gender__gender="unisex")
        )

        page = view.paginate_queryset(products)
        serializer = ListBookSerializer(page, many=True, context={"request": request})
        return view.get_paginated_response({
            "status": True,
            "results": serializer.data
        })

    brands = BrandModel.objects.filter(
        Q(gender__gender=gender) | Q(gender__gender='unisex')
    ).distinct()

    page = view.paginate_queryset(brands)
    serializer = BaseBrandSerializer(page, many=True, context={"request": request})
    return view.get_paginated_response({
        "status": True,
        "results": serializer.data
    })





def get_filtered_category_data(request, view):
    gender = request.query_params.get("gender")
    category_param = request.query_params.get("category")
    subcategory_param = request.query_params.get("subcategory")

    min_price = request.query_params.get("min_price")
    max_price = request.query_params.get("max_price")
    brand_param = request.query_params.get("brand")

    category_ids = parse_id_list(category_param)
    subcategory_ids = parse_id_list(subcategory_param)
    brand_ids = parse_id_list(brand_param)

    if subcategory_ids:
        products = BookModel.objects.filter(
            subcategory_id__in=subcategory_ids,
            subcategory__category__gender__gender__in=[gender, "unisex"]
        )

        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)
        if brand_ids:
            products = products.filter(brand_id__in=brand_ids)

        page = view.paginate_queryset(products)
        serializer = ListBookSerializer(page, many=True, context={"request": request})

        return view.get_paginated_response({
            "status": True,
            "results": serializer.data
        })

    elif category_ids:
        subcategories = SubcategoryModel.objects.filter(
            category_id__in=category_ids,
            category__gender__gender__in=[gender, "unisex"]
        )

        brands = BrandModel.objects.filter(
            category_id__in=category_ids
        ).distinct()

        subcategory_page = view.paginate_queryset(subcategories)
        subcategory_serializer = BaseSubcategorySerializer(subcategory_page, many=True, context={"request": request})

        brand_serializer = BaseBrandSerializer(brands, many=True, context={"request": request})

        return view.get_paginated_response({
            "status": True,
            "results": subcategory_serializer.data,
            "brands": brand_serializer.data
        })

    elif gender:
        categories = CategoryModel.objects.filter(
            gender__gender__in=[gender, "unisex"]
        ).distinct()

        page = view.paginate_queryset(categories)
        serializer = BaseCategorySerializer(page, many=True, context={"request": request})

        return view.get_paginated_response({
            "status": True,
            "results": serializer.data
        })

    return Response({
        "status": False,
        "message": "Kamida gender, category yoki subcategory ID yuborilishi kerak."
    }, status=400)

