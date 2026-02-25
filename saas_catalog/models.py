from django.db import models


class SaaSPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    billing_interval = models.CharField(
        max_length=20, choices=[("monthly", "Monthly"), ("yearly", "Yearly")]
    )
    features = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
