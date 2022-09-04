"""Celery tasks."""

# Django
from django.conf import settings
from django.utils import timezone

# Own
from bmat.api.models.reports import Report

# Celery
from celery.decorators import task

# Utilities
import dask.dataframe as dd
import numpy as np
import uuid
import os

@task(name='process_report', max_retries=3)
def process_report(report_id):
    """ Process input CSV file, create output file and change status report to Done. """
    
    # Get report info
    report = Report.object.get(id=report_id)

    # Read csv with Dask 
    input_data = dd.read_csv(report.input_file, parse_dates=['Date'])

    # Group data with Dask (groupby based on Pandas)
    grouped_data = input_data.groupby(['Song', 'Date']).agg(np.sum)

    # Create a output filename
    filename = "output_%s.%s" % (uuid.uuid4(), 'csv')
    output_path = os.path.join('upload', filename)

    # Save CSV file
    grouped_data.to_csv(output_path)

    # Update report info
    report.status = Report.DONE
    report.output_file = output_path
    report.save()

    print("Report {} Done".format(report.pid))



"""
    Why Dask?
    - Utilizes multiple CPU cores by internally chunking dataframe and process in parallel.
    - Can handle large datasets on a single CPU exploiting its multiple cores or cluster of machines refers to distributed computing.
    - Dask instead of computing first, create a graph of tasks which says about how to perform that task.

    Also we can use Panda with chunks. The code is below but I wanted to try this lib :)
        chunk = pd.read_csv('very_big_file.csv', chunksize=100000)
        df = pd.concat(chunk)
"""