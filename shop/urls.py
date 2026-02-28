from django.urls import path
from .views import shop_settings_view

app_name = "shop"

urlpatterns = [
    path("settings/", shop_settings_view, name="settings"),
]
