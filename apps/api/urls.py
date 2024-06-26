from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.api.views.baskets import BasketRowViewSet
from apps.api.views.items import ItemViewSet, ReviewViewSet
from apps.api.views.load_data import import_file
from apps.api.views.orders import OrderViewSet, fake_leadpay_link, notification_link

router = DefaultRouter()
router.register("items", ItemViewSet)
router.register("baskets", BasketRowViewSet)
router.register("orders", OrderViewSet)
router.register("reviews", ReviewViewSet)


urlpatterns = [
    path("auth/", include("djoser.urls.jwt")),
    path("", include("djoser.urls")),
    path("products-import-file/", import_file),
    path("", include(router.urls)),
    path("fake-leadpay-link/", fake_leadpay_link),
    path("response-leadpay-link/", notification_link),
]
