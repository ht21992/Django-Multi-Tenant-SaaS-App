from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class AuditLog(models.Model):
    user_id = models.PositiveBigIntegerField(db_index=True, null=True)
    action = models.CharField(max_length=255)
    entity = models.CharField(max_length=100)
    entity_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} by User {self.user_id} on {self.entity}"
