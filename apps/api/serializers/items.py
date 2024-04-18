from dynamic_rest.fields import DynamicMethodField, DynamicRelationField
from taggit.serializers import TaggitSerializer, TagListSerializerField

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


class ItemSerializer(TaggitSerializer, BaseModelSerializer):
    catalog = DynamicRelationField(CatalogItemSerializer, read_only=True)
    tags = TagListSerializerField()
    is_favourite = DynamicMethodField()

    class Meta:
        model = Item
        fields = [
            "id",
            "catalog",
            "price",
            "price",
            "count",
            "tags",
            "upc",
            "poster",
            "video",
            "is_active",
            "is_favourite",
        ]

    def get_is_favourite(self, obj: Item) -> bool:
        current_user = self.context["request"].user.id
        return obj.favourites.filter(id=current_user).exists()
