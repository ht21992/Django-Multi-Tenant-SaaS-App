from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "displayname", "name")
    list_filter = ()
    search_fields = ("user__username", "displayname")
    readonly_fields = ("user",)
    ordering = ("user__username",)
