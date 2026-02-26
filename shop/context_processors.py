from .models import Shop
from core.urls import is_public_schema


def tenant_branding(request):
    if is_public_schema():
        return {"branding": None}

    branding = Shop.objects.first()

    if not branding:
        return {"branding": None}

    return {
        "branding": {
            "request": request,
            "phone": branding.phone,
            "email": branding.email,
            "address": branding.address,
            "description": branding.description,
            "color": branding.color,
            "logo": branding.logo,
            "meta": branding.meta,
        }
    }
