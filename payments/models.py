from django.db import models
from orders.models import Order

class Payment(models.Model):
    PROVIDERS = [
        ("cash", "Cash"),
        ("stripe", "Stripe"),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    provider = models.CharField(max_length=20, choices=PROVIDERS)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)