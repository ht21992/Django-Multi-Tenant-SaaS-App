from django.contrib import admin
from .models import Membership


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ("user_id", "role", "is_active", "joined_at")
    list_filter = ("role", "is_active", "joined_at")
    search_fields = ("user_id",)
    readonly_fields = ("user_id", "joined_at")
    ordering = ("-joined_at",)
