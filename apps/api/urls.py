from django.urls import include, path

from apps.api.views.load_data import import_file

urlpatterns = [
    path("auth/", include("djoser.urls.jwt")),
    path("", include("djoser.urls")),
    path("products-import-file/", import_file),
]
