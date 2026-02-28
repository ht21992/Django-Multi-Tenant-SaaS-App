from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("htmx/cart/", views.cart_partial, name="htmx_cart"),
    path("htmx/cart/add/<int:product_id>/", views.htmx_cart_add, name="htmx_cart_add"),
    path(
        "htmx/cart/remove/<int:product_id>/",
        views.htmx_cart_remove,
        name="htmx_cart_remove",
    ),
    path("htmx/cart/clear/", views.htmx_cart_clear, name="htmx_cart_clear"),
    path("checkout/", views.checkout, name="checkout"),
    path("success/<int:order_id>/", views.order_success, name="order_success"),
    path("order/<int:order_id>/", views.order_details, name="order_details"),
    path("orders/", views.order_list, name="orders_list"),
]
