from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import connection
from django.contrib.auth import get_user_model

from memberships.models import Membership
from customers.models import Customer

User = get_user_model()


@receiver(post_save, sender=User)
def create_membership_or_customer_for_tenant_user(sender, instance, created, **kwargs):
    if not created:
        return

    # Do NOT create membership in public schema
    if connection.schema_name == "public":
        return

    if instance.is_superuser:
        Membership.objects.update_or_create(
            user=instance,
            defaults={"role": "owner"},
        )
        return

    # Default signup create customer
    Customer.objects.create(user=instance, email=instance.email)
