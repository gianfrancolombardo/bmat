"""Report model."""

# Django
from pyexpat import model
from django.db import models

# Own
from bmat.utils.models import BaseModel

# Util
import uuid
import os

class Report(BaseModel):
    """ Report model
        Model to save paths file and status.
    """

    WORKING = 0
    DONE = 1
    STATUS = [
        (WORKING, 'Working'),
        (DONE, 'Done')
    ]


    def rename_uuid(instance, filename):
        ext = filename.split('.')[-1]
        filename = "input_%s.%s" % (uuid.uuid4(), ext)
        return os.path.join('upload', filename)

    input_file = models.FileField(
        upload_to=rename_uuid,
        help_text="CSV file to process"
    )
    pid = models.TextField(
        null=True,
        help_text="Celery ID task"
    )
    output_file = models.TextField(
        null=True,
        help_text="CSV file path resulting"
    )
    status = models.PositiveSmallIntegerField(
        choices=STATUS,
        default=WORKING,
        help_text="Status could be 0: Processing, 1: Done"
    )
   
    def __str__(self):
        """Return report pid."""
        return self.pid

    class Meta:
        """Meta class."""

        ordering = ['-created', '-modified']

       