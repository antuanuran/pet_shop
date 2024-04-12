from django.contrib import admin

from .models import Attribute, Category, Item, ItemAttribute, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "id"]


class AttributeInlines(admin.TabularInline):
    model = Attribute
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "id"]
    inlines = [AttributeInlines]


class ItemAttributeInlines(admin.TabularInline):
    model = ItemAttribute
    extra = 0


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["product", "price", "count", "id", "is_active"]
    inlines = [ItemAttributeInlines]
