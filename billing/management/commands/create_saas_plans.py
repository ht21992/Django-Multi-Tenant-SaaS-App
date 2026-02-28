from django.core.management.base import BaseCommand
from saas_catalog.models import SaaSPlan


class Command(BaseCommand):
    help = "Create default SaaS plans"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing plans before creating new ones",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            SaaSPlan.objects.all().delete()
            self.stdout.write(self.style.WARNING("Deleted all existing plans"))

        plans_data = [
            {
                "name": "Starter",
                "description": "Perfect for individuals and small businesses just starting out",
                "price": 29.99,
                "billing_interval": "monthly",
                "max_users": 1,
                "max_products": 10,
                "max_orders": 100,
                "features": {
                    "basic_dashboard": True,
                    "product_management": True,
                    "basic_analytics": True,
                    "email_support": True,
                    "api_access": False,
                    "custom_domain": False,
                },
                "is_active": True,
                "is_popular": False,
            },
            {
                "name": "Professional",
                "description": "For growing businesses needing more features and support",
                "price": 79.99,
                "billing_interval": "monthly",
                "max_users": 5,
                "max_products": 100,
                "max_orders": 1000,
                "features": {
                    "basic_dashboard": True,
                    "product_management": True,
                    "advanced_analytics": True,
                    "priority_email_support": True,
                    "api_access": True,
                    "custom_domain": True,
                    "team_collaboration": True,
                },
                "is_active": True,
                "is_popular": True,
            },
            {
                "name": "Enterprise",
                "description": "For large organizations with custom requirements",
                "price": 299.99,
                "billing_interval": "monthly",
                "max_users": 50,
                "max_products": 1000,
                "max_orders": 10000,
                "features": {
                    "advanced_dashboard": True,
                    "product_management": True,
                    "advanced_analytics": True,
                    "24_7_phone_support": True,
                    "api_access": True,
                    "custom_domain": True,
                    "team_collaboration": True,
                    "webhooks": True,
                    "custom_integrations": True,
                    "sso": True,
                },
                "is_active": True,
                "is_popular": False,
            },
        ]

        created_plans = []
        for plan_data in plans_data:
            plan, created = SaaSPlan.objects.get_or_create(
                name=plan_data["name"],
                defaults=plan_data,
            )
            if created:
                created_plans.append(plan.name)
                self.stdout.write(self.style.SUCCESS(f"✓ Created plan: {plan.name}"))
            else:
                # Update existing plan
                for key, value in plan_data.items():
                    if key != "name":
                        setattr(plan, key, value)
                plan.save()
                self.stdout.write(self.style.WARNING(f"◷ Updated plan: {plan.name}"))

        self.stdout.write(
            self.style.SUCCESS(f"\n✓ Successfully processed {len(plans_data)} plans")
        )
        if created_plans:
            self.stdout.write(
                self.style.SUCCESS(
                    f"✓ Created {len(created_plans)} new plans: {', '.join(created_plans)}"
                )
            )
