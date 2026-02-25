from django.db import models
from tenants.models import Tenant
from saas_catalog.models import SaaSPlan


class Subscription(models.Model):
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE)
    plan = models.ForeignKey(SaaSPlan, on_delete=models.PROTECT)
    active = models.BooleanField(default=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ends_at = models.DateTimeField(null=True, blank=True)
