from django.contrib import admin
from .models import BusinessLead, Subscription


@admin.register(BusinessLead)
class BusinessLeadAdmin(admin.ModelAdmin):
    list_display = ("email", "user_id", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("email", "user_id")
    readonly_fields = ("user_id", "email", "created_at", "updated_at")
    fields = ("user_id", "email", "status", "created_at", "updated_at")
    ordering = ("-created_at",)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("tenant", "plan", "active", "started_at")
    list_filter = ("active", "plan", "started_at")
    search_fields = ("tenant__name",)
    readonly_fields = ("started_at",)
    ordering = ("-started_at",)
