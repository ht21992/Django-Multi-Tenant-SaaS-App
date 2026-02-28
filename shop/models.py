from django.db import models
from colorfield.fields import ColorField


class Shop(models.Model):
    BUSINESS_TYPES = [
        ("coffee_shop", "Coffee Shop"),
        ("restaurant", "Restaurant"),
        ("pizza", "Pizza Place"),
        ("online_shop", "Online Shop"),
        ("car_shop", "Car Shop"),
        ("other", "Other"),
    ]
    name = models.CharField(max_length=255)
    business_type = models.CharField(max_length=50, choices=BUSINESS_TYPES)
    color = ColorField(default="#1f2937")
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to="site_logos/", blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    timezone = models.CharField(max_length=50, default="UTC")
    currency = models.CharField(max_length=10, default="USD")
    meta = models.JSONField(blank=True, null=True, default=dict)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def validate_meta(self):
        if not self.meta:
            self.meta = {}

    def save(self, *args, **kwargs):
        self.validate_meta()
        super().save(*args, **kwargs)
