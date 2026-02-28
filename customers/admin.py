from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("user_id", "email", "name", "created_at")
    list_filter = ("created_at",)
    search_fields = ("email", "name", "user_id")
    readonly_fields = ("user_id", "created_at")
    ordering = ("-created_at",)
