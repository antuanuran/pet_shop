from django.contrib import admin
from django.db.models import Count

from .models import Attribute, Catalog, Category, Item, ItemAttribute, Product, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "id"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "id"]


class AttributeInlines(admin.TabularInline):
    model = Attribute
    extra = 0


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ["name", "product", "id"]
    inlines = [AttributeInlines]
    search_fields = ["name"]


class ItemAttributeInlines(admin.TabularInline):
    model = ItemAttribute
    extra = 0


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["catalog", "price", "count", "photo", "video_link", "is_active", "id", "attributes", "tag_list"]
    inlines = [ItemAttributeInlines, ReviewInline]
    autocomplete_fields = ["catalog"]
    filter_horizontal = ["favourites"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(tag_list=Count("tags"))
        return qs

    @admin.display(description="теги", ordering="tag_list")
    def tag_list(self, obj):
        return obj.tag_list

    @admin.display(boolean=True)
    def photo(self, obj):
        if obj.poster:
            return True
        else:
            return False

    @admin.display(boolean=True, description="video")
    def video_link(self, obj):
        if obj.video:
            return True
        else:
            return False
