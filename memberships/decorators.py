# memberships/decorators.py
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from .models import Membership
from django.db import connection


def role_required(*allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if connection.schema_name == "public":
                if not request.user.is_superuser:
                    return redirect("public_pages:index")

            try:
                membership = Membership.objects.get(user_id=request.user.id)

                request.membership = membership
            except Membership.DoesNotExist:
                messages.error(request, "You do not belong to this tenant")
                return redirect("tenant_pages:index")

            if membership.role not in allowed_roles:
                messages.error(request, "You do not have permission")
                return redirect("tenant_pages:index")

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
