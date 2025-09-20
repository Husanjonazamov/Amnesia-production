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
    
    
def get_filtered_data(request, view):
    gender = request.query_params.get("gender")
    category_param = request.query_params.get("category")
    subcategory_param = request.query_params.get("subcategory")
    childcategory_param = request.query_params.get("childcategory")
    brand_param = request.query_params.get("brand")

    min_price = request.query_params.get("min_price")
    max_price = request.query_params.get("max_price")

    category_ids = parse_id_list(category_param)
    subcategory_ids = parse_id_list(subcategory_param)
    childcategory_ids = parse_id_list(childcategory_param)
    brand_ids = parse_id_list(brand_param)

    # 🔹 1) BRAND YUBORILGAN HOLAT → PRODUCT
    if brand_ids:
        products = BookModel.objects.filter(brand_id__in=brand_ids)

        if childcategory_ids:
            products = products.filter(childcategories__id__in=childcategory_ids)

        if subcategory_ids:
            products = products.filter(subcategory_id__in=subcategory_ids)

        if category_ids:
            products = products.filter(subcategory__category_id__in=category_ids)

        if gender:
            products = products.filter(Q(gender__gender=gender) | Q(gender__gender="unisex"))

        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)

        products = products.distinct()
        page = view.paginate_queryset(products)
        serializer = ListBookSerializer(page, many=True, context={"request": request})

        return view.get_paginated_response({
            "status": True,
            "type": "products",
            "results": serializer.data
        })

    # 🔹 2) CHILDCATEGORY YUBORILGAN HOLAT → BRANDS
    elif childcategory_ids:
        brands = BrandModel.objects.filter(
            products__childcategories__id__in=childcategory_ids
        ).distinct()

        page = view.paginate_queryset(brands)
        serializer = BaseBrandSerializer(page, many=True, context={"request": request})

        return view.get_paginated_response({
            "status": True,
            "type": "brands",
            "results": serializer.data
        })

    # 🔹 3) SUBCATEGORY YUBORILGAN HOLAT → CHILDCATEGORIES
    elif subcategory_ids:
        from core.apps.havasbook.models.childcategory import ChildcategoryModel
        childcategories = ChildcategoryModel.objects.filter(
            subcategory_id__in=subcategory_ids
        ).distinct()

        child_page = view.paginate_queryset(childcategories)
        from core.apps.havasbook.serializers.childcategory import BaseChildcategorySerializer
        child_serializer = BaseChildcategorySerializer(child_page, many=True, context={"request": request})

        return view.get_paginated_response({
            "status": True,
            "type": "childcategories",
            "results": child_serializer.data
        })

    # 🔹 4) CATEGORY YUBORILGAN HOLAT → SUBCATEGORIES + BRANDS
    elif category_ids:
        subcategories = SubcategoryModel.objects.filter(
            category_id__in=category_ids,
            category__gender__gender__in=[gender, "unisex"]
        ).distinct()

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

    # 🔹 5) FAQAT GENDER YUBORILGAN HOLAT → CATEGORIES
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

    # 🔹 6) HECH NIMA YUBORILMAGAN HOLAT
    return Response({
        "status": False,
        "message": "Kamida gender, category, subcategory, childcategory yoki brand ID yuborilishi kerak."
    }, status=400)
