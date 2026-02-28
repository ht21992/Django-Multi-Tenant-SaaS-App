from core.urls import is_public_schema
from billing.models import Subscription
from tenants.models import Domain


def tenant_subscription(request):
    if not is_public_schema():
        return {"current_subscription": None}

    if not request.user.is_authenticated:
        return {"current_subscription": None}

    sub = Subscription.objects.filter(business_lead_user_id=request.user.id).first()

    if not sub:
        return {"current_subscription": None}

    # Get tenant domain
    tenant_domain = Domain.objects.filter(tenant=sub.tenant).first()

    # Build a rich context object
    subscription_data = {
        "subscription": sub,
        "tenant": sub.tenant,
        "plan": sub.plan,
        "domain": tenant_domain,
        "is_active": sub.active,
        "tenant_is_active": sub.tenant.is_active,
    }

    return {"current_subscription": subscription_data}
