from django.db import models


class SaaSPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    billing_interval = models.CharField(
        max_length=20, choices=[("monthly", "Monthly"), ("yearly", "Yearly")]
    )
    # Plan limits
    max_users = models.IntegerField(
        default=1, help_text="Maximum number of team members"
    )
    max_products = models.IntegerField(
        default=10, help_text="Maximum number of products"
    )
    max_orders = models.IntegerField(
        default=100, help_text="Maximum number of orders per month"
    )
    # Features
    features = models.JSONField(
        default=dict, help_text="JSON object with feature flags"
    )
    is_active = models.BooleanField(default=True)
    is_popular = models.BooleanField(
        default=False, help_text="Mark as popular plan badge"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("price",)

    def __str__(self):
        return f"{self.name} - ${self.price}/{self.billing_interval}"
