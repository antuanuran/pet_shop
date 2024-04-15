from django.contrib import admin

from .models import Attribute, Catalog, Category, Item, ItemAttribute, Product


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


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["catalog", "price", "count", "photo", "video_link", "is_active", "id", "attributes"]
    inlines = [ItemAttributeInlines]
    autocomplete_fields = ["catalog"]

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
