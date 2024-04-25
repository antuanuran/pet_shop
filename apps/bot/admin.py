from django.contrib import admin

from apps.bot.models import TgUser


@admin.register(TgUser)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "username"]
