from django.contrib import admin
from .models import Membership


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "is_active")
    list_filter = ("role", "is_active")
