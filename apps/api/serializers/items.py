from dynamic_rest.fields import DynamicRelationField

from apps.api.serializers.abstract_dynamic import BaseModelSerializer
from apps.products.models import Catalog, Item, Product


class ProductItemSerializer(BaseModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "category"]


class CatalogItemSerializer(BaseModelSerializer):
    product = DynamicRelationField(ProductItemSerializer, read_only=True)

    class Meta:
        model = Catalog
        fields = ["id", "name", "product"]


class ItemSerializer(BaseModelSerializer):
    catalog = DynamicRelationField(CatalogItemSerializer, read_only=True)

    class Meta:
        model = Item
        fields = [
            "catalog",
            "price",
            "price",
            "count",
            "upc",
            "poster",
            "video",
            "is_active",
        ]
