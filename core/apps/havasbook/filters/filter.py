from django.db.models import Q
from core.apps.havasbook.models import BookModel, BrandModel, CategoryModel, SubcategoryModel
from core.apps.havasbook.serializers import (
    BaseBrandSerializer, BaseCategorySerializer, BaseSubcategorySerializer, ListBookSerializer
)
from rest_framework.response import Response
import re


def parse_id_list(param):
    """Query param ichidan raqamlar ro'yxatini olish"""
    if not param:
        return []
    return list(map(int, re.findall(r'\d+', param)))


def get_filtered_data(request, view):
    gender = request.query_params.get("gender")
    category_param = request.query_params.get("category")
    subcategory_param = request.query_params.get("subcategory")
    brand_param = request.query_params.get("brand")

    min_price = request.query_params.get("min_price")
    max_price = request.query_params.get("max_price")

    category_ids = parse_id_list(category_param)
    subcategory_ids = parse_id_list(subcategory_param)
    brand_ids = parse_id_list(brand_param)

    # 1️⃣ BRAND YUBORILGAN HOLAT
    if brand_ids:
        products = BookModel.objects.filter(
            brand_id__in=brand_ids
        ).filter(
            Q(gender__gender=gender) | Q(gender__gender="unisex")
        )

        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)

        page = view.paginate_queryset(products)
        serializer = ListBookSerializer(page, many=True, context={"request": request})
        return view.get_paginated_response({
            "status": True,
            "type": "products",
            "results": serializer.data
        })

    # 2️⃣ SUBCATEGORY YUBORILGAN HOLAT
    elif subcategory_ids:
        # Faqat shu subcategory ichida product mavjud bo‘lgan brandlar
        brands = BrandModel.objects.filter(
            products__subcategory_id__in=subcategory_ids
        ).distinct()

        page = view.paginate_queryset(brands)
        serializer = BaseBrandSerializer(page, many=True, context={"request": request})

        return view.get_paginated_response({
            "status": True,
            "type": "brands",
            "results": serializer.data
        })

    # 3️⃣ CATEGORY YUBORILGAN HOLAT
    elif category_ids:
        subcategories = SubcategoryModel.objects.filter(
            category_id__in=category_ids,
            category__gender__gender__in=[gender, "unisex"]
        ).distinct()

        # Faqat product mavjud bo‘lgan brandlar
        brands = BrandModel.objects.filter(
            products__subcategory__category_id__in=category_ids
        ).distinct()

        sub_page = view.paginate_queryset(subcategories)
        sub_serializer = BaseSubcategorySerializer(sub_page, many=True, context={"request": request})

        brand_serializer = BaseBrandSerializer(brands, many=True, context={"request": request})

        return view.get_paginated_response({
            "status": True,
            "type": "subcategories_and_brands",
            "subcategories": sub_serializer.data,
            "brands": brand_serializer.data
        })

    # 4️⃣ FAQAT GENDER YUBORILGAN HOLAT
    elif gender:
        categories = CategoryModel.objects.filter(
            gender__gender__in=[gender, "unisex"]
        ).distinct()

        page = view.paginate_queryset(categories)
        serializer = BaseCategorySerializer(page, many=True, context={"request": request})

        return view.get_paginated_response({
            "status": True,
            "type": "categories",
            "results": serializer.data
        })

    # 5️⃣ PARAMETRLAR YO‘Q BO‘LSA
    return Response({
        "status": False,
        "message": "Kamida gender, category, subcategory yoki brand ID yuborilishi kerak."
    }, status=400)
