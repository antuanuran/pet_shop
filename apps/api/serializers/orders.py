from dynamic_rest.fields import DynamicRelationField
from rest_framework.exceptions import PermissionDenied

from apps.api.serializers.abstract_dynamic import BaseModelSerializer
from apps.api.serializers.items import ItemSerializer
from apps.orders.models import Order, OrderRow


class OrderRowSerializer(BaseModelSerializer):
    item = DynamicRelationField(ItemSerializer, read_only=True)

    class Meta:
        model = OrderRow
        fields = [
            "id",
            "item",
            "qty",
            "price",
        ]
        extra_kwargs = {"item": {"read_only": True}}


class OrderSerializer(BaseModelSerializer):
    spisok_tovarov_zakaza = DynamicRelationField(OrderRowSerializer, read_only=True, many=True, source="order_rows")

    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "created_at",
            "updated_at",
            "spisok_tovarov_zakaza",
        ]

    def validate_status(self, value):
        if value != Order.Status.STATUS_CANCELED:
            raise PermissionDenied("User может изменять статус заказа только на 'отменён'")
        return value
