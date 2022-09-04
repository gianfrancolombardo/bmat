"""Api admin."""

# Django
from django.contrib import admin

# Models
from bmat.api.models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    
    list_display = ('pid','created')
    search_fields = ('pid',)
    list_filter = ('created',)
 