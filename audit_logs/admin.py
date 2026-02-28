from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("user_id", "action", "entity", "entity_id", "created_at")
    list_filter = ("action", "entity", "created_at")
    search_fields = ("user_id", "action", "entity", "entity_id")
    readonly_fields = ("user_id", "action", "entity", "entity_id", "created_at")
    ordering = ("-created_at",)
