from core.apps.havasbook.serializers.gender import BaseGenderSerializer
from core.apps.havasbook.serializers.brand import BaseBrandSerializer
from core.apps.havasbook.serializers.variants import BaseColorSerializer, BaseSizeSerializer




class ProductServices:
    
    @staticmethod
    def get_gender(gender_obj):
        return BaseGenderSerializer(gender_obj).data if gender_obj else None
    
    @staticmethod
    def get_brand(brand_obj):
        return BaseBrandSerializer(brand_obj).data if brand_obj else None
    
    @staticmethod
    def get_colors(colors_queryset, request):
        return BaseColorSerializer(colors_queryset, many=True, context={"request": request}).data 
    
    
    @staticmethod
    def get_image_url(image, request):
        if request and image:
            return request.build_absolute_uri(image.url)
        return None
    
    
    @staticmethod
    def get_sizes(sizes_queryset):
        return BaseSizeSerializer(sizes_queryset,many=True).data if sizes_queryset else None