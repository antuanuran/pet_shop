# from django.db import transaction
# from django.utils.decorators import method_decorator
# from drf_yasg.utils import no_body, swagger_auto_schema
# from rest_framework import status
# from rest_framework.decorators import action
# from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from apps.api.serializers.orders import OrderSerializer

# from rest_framework.response import Response
# from rest_framework.viewsets import ModelViewSet
from apps.api.views.abstract_dynamic import BaseModelViewSet
from apps.orders.models import Order


class OrderViewSet(BaseModelViewSet):
    http_method_names = [
        "get",
        "post",
        "head",
        "options",
        "patch",
    ]  # Get на сущность, Get на список, Patch на сущность. Post - разрешили, но сам create - нужно запретить

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, queryset=None):
        qs = super().get_queryset()
        result = qs.filter(user_id=self.request.user.id)
        return result
