from .views import (
    index_view,
    plan_selection_view,
    plan_checkout_view,
    subscription_view,
)
from django.urls import path

urlpatterns = [
    path("", index_view, name="index"),
    path("plans/", plan_selection_view, name="plans"),
    path("plans/<int:plan_id>/checkout/", plan_checkout_view, name="plan_checkout"),
    path("subscription/", subscription_view, name="subscription"),
]
