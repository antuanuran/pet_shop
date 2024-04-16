from rest_framework import serializers

from apps.products.models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = [
            "catalog",
            "price",
            "price",
            "count",
            "upc",
            "poster",
            "is_active",
        ]
