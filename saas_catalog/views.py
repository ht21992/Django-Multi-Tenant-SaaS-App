from django.shortcuts import render
from django.http import JsonResponse
from .models import SaaSPlan


def plans_list_view(request):
    """Display all active SaaS plans"""
    plans = SaaSPlan.objects.filter(is_active=True)
    context = {
        "plans": plans,
    }
    return render(request, "saas_catalog/plans_list.html", context)


def plans_htmx_cards_view(request):
    """HTMX endpoint for plan cards"""
    plans = SaaSPlan.objects.filter(is_active=True)
    return render(request, "saas_catalog/partials/plan_cards.html", {"plans": plans})


def plans_comparison_view(request):
    """Display plans comparison table"""
    plans = SaaSPlan.objects.filter(is_active=True)
    context = {
        "plans": plans,
    }
    return render(request, "saas_catalog/plans_comparison.html", context)


def plan_details_view(request, plan_id):
    """Display single plan details with HTMX"""
    plan = SaaSPlan.objects.get(id=plan_id)
    if request.htmx:
        return render(request, "saas_catalog/partials/plan_detail.html", {"plan": plan})
    return render(request, "saas_catalog/plan_detail.html", {"plan": plan})
