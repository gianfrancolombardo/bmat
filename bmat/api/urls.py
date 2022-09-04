"""api URLs."""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from bmat.api.views import reports as report_views

router = DefaultRouter()
router.register(r'reports', report_views.ReportViewSet, basename='report')

urlpatterns = [
    path('', include(router.urls))
]
