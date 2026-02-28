from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import connection
from django.utils import timezone
from datetime import timedelta
from saas_catalog.models import SaaSPlan
from tenants.models import Tenant, Domain
from billing.models import Subscription, BusinessLead
from django_tenants.utils import schema_context


# additional imports for subscription page
from django.http import HttpResponseRedirect

User_Model = get_user_model()


def index_view(request):
    plans = SaaSPlan.objects.filter(is_active=True)
    context = {
        "plans": plans,
    }
    return render(request, "public/index.html", context)


def plan_selection_view(request):
    """Display all active plans with HTMX support"""
    plans = SaaSPlan.objects.filter(is_active=True)
    return render(request, "public/partials/plans_grid.html", {"plans": plans})


@login_required(login_url="/accounts/login/")
def plan_checkout_view(request, plan_id):
    """Show checkout form for selected plan"""
    plan = get_object_or_404(SaaSPlan, id=plan_id, is_active=True)

    if request.method == "POST":
        schema_name = request.POST.get("schema_name", "").lower().strip()
        tenant_name = request.POST.get("tenant_name", "").strip()
        domain_name = request.POST.get("domain_name", "").lower().strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        # Validation
        errors = []

        if not schema_name:
            errors.append("Schema name is required")
        elif Tenant.objects.filter(schema_name=schema_name).exists():
            errors.append("Schema name already taken")
        elif len(schema_name) < 3:
            errors.append("Schema name must be at least 3 characters")

        if not tenant_name:
            errors.append("Business name is required")
        elif len(tenant_name) < 2:
            errors.append("Business name must be at least 2 characters")

        if not domain_name:
            errors.append("Domain is required")
        elif Domain.objects.filter(domain=domain_name).exists():
            errors.append("Domain already taken")

        if not password:
            errors.append("Password is required")
        elif len(password) < 8:
            errors.append("Password must be at least 8 characters")
        elif password != confirm_password:
            errors.append("Passwords do not match")

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(
                request,
                "public/partials/plan_checkout.html",
                {
                    "plan": plan,
                    "form_data": request.POST,
                },
            )

        try:
            # Create Tenant
            tenant = Tenant(
                schema_name=schema_name,
                name=tenant_name,
                is_active=True,
            )

            # Calculate paid_until based on plan interval
            if plan.billing_interval == "monthly":
                tenant.paid_until = timezone.now().date() + timedelta(days=30)
            else:  # yearly
                tenant.paid_until = timezone.now().date() + timedelta(days=365)

            tenant.save()

            # Create Domain
            Domain.objects.create(
                domain=domain_name,
                tenant=tenant,
                is_primary=True,
            )

            # Create Subscription in new schema
            with schema_context(tenant.schema_name):
                # Create superuser in tenant schema
                superuser = User_Model.objects.create_superuser(
                    username="admin",
                    email=(
                        request.user.email
                        if request.user.is_authenticated
                        else f"admin@{domain_name}"
                    ),
                    password=password,
                )

            # Create subscription record in public schema
            sub = Subscription.objects.create(
                tenant=tenant,
                business_lead_user_id=request.user.id,
                plan=plan,
                active=True,
                ends_at=None,
            )

            # remember which tenant we just created so the public user can
            # view its plan later
            request.session["tenant_id"] = tenant.id

            # Update BusinessLead if user was authenticated
            if request.user.is_authenticated:
                try:
                    lead = BusinessLead.objects.get(user_id=request.user.id)
                    lead.status = "converted"
                    lead.save()
                except BusinessLead.DoesNotExist:
                    pass

            messages.success(
                request,
                f"Tenant '{tenant_name}' created successfully! You can now access it at {domain_name}",
            )
            return redirect("index")

        except Exception as e:
            messages.error(request, f"Error creating tenant: {str(e)}")
            return render(
                request,
                "public/partials/plan_checkout.html",
                {
                    "plan": plan,
                    "form_data": request.POST,
                },
            )

    return render(request, "public/partials/plan_checkout.html", {"plan": plan})


@login_required(login_url="/accounts/login/")
def subscription_view(request):
    """Display user's subscription details"""
    try:
        subscription = Subscription.objects.get(business_lead_user_id=request.user.id)
        context = {
            "subscription": subscription,
        }
    except Subscription.DoesNotExist:
        context = {
            "subscription": None,
        }

    return render(request, "public/subscription.html", context)
