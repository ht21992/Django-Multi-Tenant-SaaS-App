from django.shortcuts import redirect
from django.contrib.auth import logout
from django.urls import reverse
from django.db import connection

from memberships.models import Membership


class TenantMembershipMiddleware:
    """
    Enforces:
    - User must belong to current tenant
    - Otherwise logout and redirect to login
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Public schema → ignore
        if connection.schema_name == "public":
            return self.get_response(request)

        if request.user.is_authenticated:
            if not Membership.objects.filter(
                user_id=request.user.id, is_active=True
            ).exists():
                logout(request)
                return redirect(reverse("account_login"))

        return self.get_response(request)
