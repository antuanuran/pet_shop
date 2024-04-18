from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.api.views.baskets import BasketRowViewSet
from apps.api.views.items import ItemViewSet
from apps.api.views.load_data import import_file

router = DefaultRouter()
router.register("items", ItemViewSet)
router.register("baskets", BasketRowViewSet)

urlpatterns = [
    path("auth/", include("djoser.urls.jwt")),
    path("", include("djoser.urls")),
    path("products-import-file/", import_file),
    path("", include(router.urls)),
]
