from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import connection
from memberships.decorators import role_required
from .models import Shop


@role_required("owner", "admin")
def shop_settings_view(request):
    """Display and handle shop settings form"""
    if connection.schema_name == "public":
        return redirect("account_login")

    # Get or create shop for this tenant
    shop, created = Shop.objects.get_or_create(id=1)

    if request.method == "POST":
        shop.name = request.POST.get("name", shop.name)
        shop.business_type = request.POST.get("business_type", shop.business_type)
        shop.description = request.POST.get("description", shop.description)
        shop.phone = request.POST.get("phone", shop.phone)
        shop.email = request.POST.get("email", shop.email)
        shop.address = request.POST.get("address", shop.address)
        shop.timezone = request.POST.get("timezone", shop.timezone)
        shop.currency = request.POST.get("currency", shop.currency)
        shop.color = request.POST.get("color", shop.color)
        shop.tax_rate = request.POST.get("tax_rate", shop.tax_rate)

        # Handle meta fields
        if not shop.meta:
            shop.meta = {}

        # Update meta fields
        shop.meta["brand_gradient_from"] = request.POST.get(
            "brand_gradient_from", shop.meta.get("brand_gradient_from", "")
        )
        shop.meta["brand_gradient_to"] = request.POST.get(
            "brand_gradient_to", shop.meta.get("brand_gradient_to", "")
        )
        shop.meta["brand_light"] = request.POST.get(
            "brand_light", shop.meta.get("brand_light", "")
        )
        shop.meta["brand_medium"] = request.POST.get(
            "brand_medium", shop.meta.get("brand_medium", "")
        )

        # Handle logo upload
        if "logo" in request.FILES:
            shop.logo = request.FILES["logo"]

        shop.save()
        messages.success(request, "Shop settings updated successfully!")
        return redirect("index")

    context = {
        "shop": shop,
        "business_types": Shop.BUSINESS_TYPES,
    }
    return render(request, "shop/settings.html", context)
