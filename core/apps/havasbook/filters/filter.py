from django.db.models import Q
from core.apps.havasbook.models import BookModel, BrandModel, CategoryModel, SubcategoryModel
from core.apps.havasbook.serializers import (
    BaseBrandSerializer, BaseCategorySerializer, BaseSubcategorySerializer, ListBookSerializer, BaseChildcategorySerializer
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
    



def get_filtered_data(request, paginator, view=None):
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

    # 📌 Filter qo‘llash uchun umumiy funksiya
    def apply_common_filters(queryset):
        if gender:
            queryset = queryset.filter(Q(gender__gender=gender) | Q(gender__gender="unisex"))
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        return queryset.distinct()

    # -------- Agar brand yuborilgan bo‘lsa --------
    if brand_ids:
        products = BookModel.objects.filter(brand_id__in=brand_ids)
        if childcategory_ids:
            products = products.filter(childcategories__id__in=childcategory_ids)
        if subcategory_ids:
            products = products.filter(
                Q(subcategory_id__in=subcategory_ids) |
                Q(childcategories__subcategory_id__in=subcategory_ids)
            )
        if category_ids:
            products = products.filter(
                Q(subcategory__category_id__in=category_ids) |
                Q(childcategories__subcategory__category_id__in=category_ids)
            )

        products = apply_common_filters(products)

        page = paginator.paginate_queryset(products, request, view=view)
        serializer = ListBookSerializer(page, many=True, context={"request": request})

        return paginator.get_paginated_response({
            "status": True,
            "type": "products",
            "results": serializer.data
        })

    # -------- Agar childcategory yuborilgan bo‘lsa --------
    elif childcategory_ids:
        from core.apps.havasbook.models.childcategory import ChildcategoryModel
        from core.apps.havasbook.serializers.childcategory import BaseChildcategorySerializer

        childcategories = ChildcategoryModel.objects.filter(
            id__in=childcategory_ids, products__isnull=False
        ).distinct()

        products = BookModel.objects.filter(childcategories__id__in=childcategory_ids)
        products = apply_common_filters(products)

        brands = BrandModel.objects.filter(products__childcategories__id__in=childcategory_ids).distinct()

        page_product = paginator.paginate_queryset(products, request, view=view)
        product_serializer = ListBookSerializer(page_product, many=True, context={"request": request})
        brand_serializer = BaseBrandSerializer(brands, many=True, context={"request": request})
        child_serializer = BaseChildcategorySerializer(childcategories, many=True, context={"request": request})

        return paginator.get_paginated_response({
            "status": True,
            "type": "childcategories_brands_products",
            "childcategories": child_serializer.data,
            "brands": brand_serializer.data,
            "products": product_serializer.data
        })

    # -------- Agar subcategory yuborilgan bo‘lsa --------
    elif subcategory_ids:
        from core.apps.havasbook.models.childcategory import ChildcategoryModel
        from core.apps.havasbook.serializers.childcategory import BaseChildcategorySerializer

        childcategories = ChildcategoryModel.objects.filter(
            subcategory_id__in=subcategory_ids, products__isnull=False
        ).distinct()

        # ✅ Mahsulotlar — to‘g‘ridan-to‘g‘ri yoki child orqali
        products = BookModel.objects.filter(
            Q(subcategory_id__in=subcategory_ids) |
            Q(childcategories__subcategory_id__in=subcategory_ids)
        )
        products = apply_common_filters(products)

        # ✅ Brandlar — to‘g‘ridan-to‘g‘ri yoki child orqali
        brands = BrandModel.objects.filter(
            Q(products__subcategory_id__in=subcategory_ids) |
            Q(products__childcategories__subcategory_id__in=subcategory_ids)
        ).distinct()

        child_serializer = BaseChildcategorySerializer(childcategories, many=True, context={"request": request})
        brand_serializer = BaseBrandSerializer(brands, many=True, context={"request": request})

        product_page = paginator.paginate_queryset(products, request, view=view)
        product_serializer = ListBookSerializer(product_page, many=True, context={"request": request})

        return paginator.get_paginated_response({
            "status": True,
            "type": "subcategories_brands_products",
            "childcategories": child_serializer.data,
            "brands": brand_serializer.data,
            "products": product_serializer.data
        })

    # -------- Agar category yuborilgan bo‘lsa --------
    elif category_ids:
        subcategories = SubcategoryModel.objects.filter(category_id__in=category_ids).distinct()

        # ✅ Mahsulotlar — to‘g‘ridan-to‘g‘ri yoki child orqali
        products = BookModel.objects.filter(
            Q(subcategory__category_id__in=category_ids) |
            Q(childcategories__subcategory__category_id__in=category_ids)
        )
        products = apply_common_filters(products)

        # ✅ Brandlar — hammasi
        brands = BrandModel.objects.filter(
            Q(products__subcategory__category_id__in=category_ids) |
            Q(products__childcategories__subcategory__category_id__in=category_ids)
        ).distinct()

        sub_serializer = BaseSubcategorySerializer(subcategories, many=True, context={"request": request})
        brand_serializer = BaseBrandSerializer(brands, many=True, context={"request": request})

        product_page = paginator.paginate_queryset(products, request, view=view)
        product_serializer = ListBookSerializer(product_page, many=True, context={"request": request})

        return paginator.get_paginated_response({
            "status": True,
            "type": "categories_subcategories_brands_products",
            "subcategories": sub_serializer.data,
            "brands": brand_serializer.data,
            "products": product_serializer.data
        })

    # -------- Agar faqat gender yuborilgan bo‘lsa --------
    elif gender:
        categories = CategoryModel.objects.filter(
            gender__gender__in=[gender, "unisex"]
        ).distinct()

        brands = BrandModel.objects.filter(
            Q(products__subcategory__category__gender__gender__in=[gender, "unisex"]) |
            Q(products__childcategories__subcategory__category__gender__gender__in=[gender, "unisex"])
        ).distinct()

        products = BookModel.objects.filter(
            Q(gender__gender=gender) | Q(gender__gender="unisex")
        ).distinct()

        products = apply_common_filters(products)

        cat_serializer = BaseCategorySerializer(categories, many=True, context={"request": request})
        brand_serializer = BaseBrandSerializer(brands, many=True, context={"request": request})

        product_page = paginator.paginate_queryset(products, request, view=view)
        product_serializer = ListBookSerializer(product_page, many=True, context={"request": request})

        return paginator.get_paginated_response({
            "status": True,
            "type": "categories_brands_products",
            "categories": cat_serializer.data,
            "brands": brand_serializer.data,
            "products": product_serializer.data
        })

    # ❌ Agar hech qanday filter yuborilmasa
    return Response({
        "status": False,
        "message": "Kamida gender, category, subcategory, childcategory yoki brand ID yuborilishi kerak."
    }, status=400)
