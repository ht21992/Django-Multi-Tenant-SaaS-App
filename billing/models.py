from django.db import models
from django.conf import settings
from tenants.models import Tenant
from saas_catalog.models import SaaSPlan

User = settings.AUTH_USER_MODEL


class BusinessLead(models.Model):
    """Track signups in public schema as business leads"""

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("converted", "Converted"),
    ]

    user_id = models.PositiveBigIntegerField(db_index=True, unique=True)
    email = models.EmailField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Business Lead"
        verbose_name_plural = "Business Leads"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.email} ({self.status})"


class Subscription(models.Model):
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE)
    business_lead_user_id = models.PositiveBigIntegerField(db_index=True, unique=True)
    plan = models.ForeignKey(SaaSPlan, on_delete=models.PROTECT)
    active = models.BooleanField(default=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ends_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.tenant.name} - {self.plan.name}"
