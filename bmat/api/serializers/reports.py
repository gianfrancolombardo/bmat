"""Reports serializers."""

# Django
from django.core.validators import FileExtensionValidator

# Django Rest Framework
from rest_framework import serializers

# Own
from bmat.api.models import Report
from bmat.taskapp.tasks import process_report

class ReportCreateSerializer(serializers.Serializer):
    """ Report create serializer
        Handle data validation, create a report, and return pid task
    """
    
    pid = serializers.CharField(read_only=True)
    input_file = serializers.FileField(
        write_only=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['csv']),
        ]
    )

    def validate(self, data):
        """ Validation CSV file structure before create. """
        delimiter = ','
        """with open(data['input']) as f:
            first_line = f.readlines()[0].rstrip()
            second_line = f.readlines()[1].rstrip()

            if (len(first_line.split(delimiter)) != 3):
                raise serializers.ValidationError(
                    {"input", "File isn't in the expected format"}
                )
        """
        return data


    def create(self, data):
        """ Create a ticket object."""

        report = Report.objects.create(**data)
        celery_task = process_report.delay(report.id)

        report.pid = celery_task.id
        data['pid'] = report.pid
        report.save()

        return data


class ReportStatusSerializer(serializers.ModelSerializer):
    """ Status report serializer
        Structure to serve report's status
    """

    class Meta:
        model = Report
        fields = [
            'pid',
            'status',
            'output_file'
        ]