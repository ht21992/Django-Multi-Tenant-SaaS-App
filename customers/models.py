from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Customer(models.Model):
    user_id = models.PositiveBigIntegerField(db_index=True, null=True, blank=True)
    email = models.EmailField()
    name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User {self.user_id} ({self.email})"
