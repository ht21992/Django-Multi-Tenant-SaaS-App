from django.urls import path
from . import views

app_name = "saas_catalog"

urlpatterns = [
    path("plans/", views.plans_list_view, name="plans_list"),
    path("plans/comparison/", views.plans_comparison_view, name="plans_comparison"),
    path("plans/htmx-cards/", views.plans_htmx_cards_view, name="plans_htmx_cards"),
    path("plans/<int:plan_id>/", views.plan_details_view, name="plan_detail"),
]
