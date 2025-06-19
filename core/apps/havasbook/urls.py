from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.apps.havasbook.views import (
    BannerView,
    CategoryView,
    BookView,
    CartitemView,
    CartView,
    LocationView,
    OrderView, 
    OrderitemView,
    BooksSearchView,
    PreorderView,
    DeliveryView,
    GenderView,
    BrandView,
    SubcategoryView
    

)

router = DefaultRouter()
router.register(r"banner", BannerView, basename='banner')
router.register(r"product", BookView, basename='product')
router.register(r"cart", CartView, basename='cart')
router.register(r"cart-item", CartitemView, basename='cart-item')
router.register(r"location", LocationView, basename='location')
router.register(r"order", OrderView, basename='order')
router.register(r"order-item", OrderitemView, basename='order-item')
router.register(r"preorder", PreorderView, basename="preorder")
router.register(r"delivery", DeliveryView, basename='delivery')

# kategorylar
router.register(r"category", CategoryView, basename='category')
router.register(r"subcategory", SubcategoryView, basename="subcategory")
router.register(r"brand", BrandView, basename="brand")
router.register(r"gender", GenderView, basename="gender")



# search
router.register(r"search", BooksSearchView, basename="search")




urlpatterns = [
    path("", include(router.urls)),
]
