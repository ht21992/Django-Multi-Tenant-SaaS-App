from django.contrib import admin
from .models import Shop


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name",)
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
