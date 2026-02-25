from django_tenants.models import TenantMixin, DomainMixin
from django.db import models


class Tenant(TenantMixin):
    name = models.CharField(max_length=255)
    paid_until = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    auto_create_schema = True


class Domain(DomainMixin):
    pass
