"""Main URLs module."""

from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    # Django Admin
    path(settings.ADMIN_URL, admin.site.urls),

    path('api/', include(('bmat.api.urls', 'api'), namespace='apis')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
