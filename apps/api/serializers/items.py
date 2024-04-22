from dynamic_rest.fields import DynamicMethodField, DynamicRelationField
from taggit.serializers import TaggitSerializer, TagListSerializerField

from apps.api.serializers.abstract_dynamic import BaseModelSerializer
from apps.api.serializers.holder import ImageHolderSerializer, VideoHolderSerializer
from apps.products.models import Catalog, Item, Product, Review
from apps.users.models import User


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


class UserSerializerMini(BaseModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email"]


class ReviewSerializer(BaseModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "author", "item", "text", "rating", "images", "videos"]

    author = DynamicRelationField(UserSerializerMini, read_only=True)
    item = DynamicRelationField(ItemSerializer)
    images = DynamicRelationField(ImageHolderSerializer, many=True)
    videos = DynamicRelationField(VideoHolderSerializer, many=True)

    # def validate_text(self, value: str) -> str:
    #     blacklisted_words = BlacklistedWord.objects.values_list("word", flat=True)
    #     if not blacklisted_words:
    #         return value
    #     blacklisted_words = "|".join(blacklisted_words)
    #     pattern = re.compile(blacklisted_words, re.IGNORECASE)
    #     return pattern.sub("***", value)
