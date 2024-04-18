# from rest_framework import serializers
from dynamic_rest.fields import DynamicRelationField
from rest_framework import serializers

from apps.api.serializers.abstract_dynamic import BaseModelSerializer
from apps.api.serializers.items import ItemSerializer
from apps.baskets.models import Basket, BasketRow

# from apps.products.models import Item
from apps.users.models import User

# from rest_framework.exceptions import ValidationError


class UserSerializer(BaseModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email"]


class BasketSerializer(BaseModelSerializer):
    user = DynamicRelationField(UserSerializer, read_only=True)

    class Meta:
        model = Basket
        fields = ["id", "user"]


class BasketRowSerializer(BaseModelSerializer):
    item = DynamicRelationField(ItemSerializer)
    qty = serializers.IntegerField()
    basket = DynamicRelationField(BasketSerializer, read_only=True)

    class Meta:
        model = BasketRow
        fields = ["basket", "qty", "item", "id"]
        extra_kwargs = {"basket": {"read_only": True}}

    # def validate(self, attrs):
    #     if not Item.objects.filter(id=attrs["item"], is_active=True).exists():
    #         raise ValidationError("Данного товара не существует!", code="no-item_id")
    #     else:
    #         return attrs

    # def create(self, validated_data):    #
    #     item_id = validated_data["item_id"]
    #     basket_id = validated_data["basket_id"]
    #
    #     exist_row = BasketRow.objects.filter(item_id=item_id, basket_id=basket_id).first()
    #     if exist_row:
    #         new_qty = exist_row.qty + validated_data["qty"]
    #         if new_qty > exist_row.item.count:
    #             raise ValidationError(f"too many items! Total: {exist_row.item.count}")
    #
    #         exist_row.qty = new_qty
    #         exist_row.save()
    #         return exist_row
    #
    #     item = Item.objects.get(id=validated_data["item_id"])
    #     if validated_data["qty"] > item.count:
    #         raise ValidationError(f"too many items! Total: {item.count}")
    #
    #     return super().create(validated_data)
