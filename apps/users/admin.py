from django.contrib import admin

from apps.products.models import Item
from apps.users.models import User


class FavouriteInline(admin.TabularInline):
    model = Item.favourites.through
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "id"]
    inlines = [FavouriteInline]
