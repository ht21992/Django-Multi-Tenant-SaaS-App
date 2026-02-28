from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ("product_name", "product_id", "quantity", "unit_price")
    readonly_fields = ("product_name", "product_id", "quantity", "unit_price")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "status", "total_amount", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("id", "customer__email")
    readonly_fields = ("created_at",)
    inlines = [OrderItemInline]
    ordering = ("-created_at",)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product_name", "product_id", "quantity", "unit_price")
    list_filter = ("order__created_at",)
    search_fields = ("order__id", "product_name", "product_id")
    readonly_fields = ("order", "product_name", "product_id", "quantity", "unit_price")
