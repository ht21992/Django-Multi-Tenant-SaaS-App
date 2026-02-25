from django.db import models
from products.models import Product


class InventoryItem(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    low_stock_threshold = models.PositiveIntegerField(default=5)

    updated_at = models.DateTimeField(auto_now=True)
