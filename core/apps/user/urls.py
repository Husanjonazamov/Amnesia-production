from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.apps.user.views import UserView

router = DefaultRouter()
router.register(r"create", UserView, basename='user')


urlpatterns = [
    path("", include(router.urls)),
]
