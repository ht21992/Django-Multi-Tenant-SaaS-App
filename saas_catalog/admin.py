from django.contrib import admin
from .models import SaaSPlan


@admin.register(SaaSPlan)
class SaaSPlanAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "billing_interval",
        "max_users",
        "is_active",
        "is_popular",
    )
    list_filter = ("is_active", "is_popular", "billing_interval", "created_at")
    search_fields = ("name", "description")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Basic Info", {"fields": ("name", "description", "is_active", "is_popular")}),
        ("Pricing", {"fields": ("price", "billing_interval")}),
        ("Plan Limits", {"fields": ("max_users", "max_products", "max_orders")}),
        ("Features", {"fields": ("features",)}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
    ordering = ("price",)
