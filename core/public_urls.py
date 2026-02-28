from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from users.views import profile_view
from django.db import connection
from tenants.admin import tenant_admin_site


def is_public_schema():
    return connection.schema_name == "public"


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("profile/", include("users.urls")),
    path("@<username>/", profile_view, name="profile"),
    path("admin_tenants/", tenant_admin_site.urls),
    path("", include("public_pages.urls")),

]


# Only used when DEBUG=True, whitenoise can serve files when DEBUG=False
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
