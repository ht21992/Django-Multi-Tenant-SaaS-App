from .views import index_view
from django.urls import path

app_name = "public_pages"

urlpatterns = [
    path("", index_view, name="index"),
]
