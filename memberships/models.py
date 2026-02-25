from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Membership(models.Model):
    ROLE_CHOICES = [
        ("owner", "Owner"),
        ("admin", "Admin"),
        ("staff", "Staff"),
        ("viewer", "Viewer"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user",)

    def __str__(self):
        return f"{self.user} ({self.role})"
