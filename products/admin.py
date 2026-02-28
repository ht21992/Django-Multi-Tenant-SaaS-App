from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "price", "is_active", "created_at")
    list_filter = ("is_active", "type", "created_at")
    search_fields = ("name", "description")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
