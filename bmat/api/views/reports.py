"""Reports views."""

# Django Rest Framework
from asyncio import constants
from rest_framework import viewsets, status, mixins

# Own
from bmat.api.serializers import ReportCreateSerializer, ReportStatusSerializer
from bmat.api.models import Report

class ReportViewSet(mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    """ Report viewset
        Handle creating and retrieving report
    """

    lookup_field ='pid'
    queryset = Report.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return ReportCreateSerializer
        if self.action == 'retrieve':
            return ReportStatusSerializer