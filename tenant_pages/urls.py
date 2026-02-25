from .views import index_view, create_product_view
from django.urls import path

urlpatterns = [
    path("", index_view, name="index"),
    path("create-product/", create_product_view, name="create-product"),
]
