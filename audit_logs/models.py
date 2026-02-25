from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class AuditLog(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=255)
    entity = models.CharField(max_length=100)
    entity_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
