""" Report tests. """

# Django
from django.core.files.uploadedfile import SimpleUploadedFile

# Django REST Framework
from rest_framework import status
from rest_framework.test import APITestCase

# Model
from bmat.api.models import Report

class ReportAPITestCase(APITestCase):
    """ Reports API test case. """

    def setUp(self):
        self.url = '/reports/'
        input_file_ok = open('./data to test/test_small.csv', 'rb')
        input_data_ok = SimpleUploadedFile(content = input_file_ok.read(), name=input_file_ok.name, content_type='multipart/form-data')
        input_file_error = open('./data to test/test_small_error.csv', 'rb')
        input_data_error = SimpleUploadedFile(content = input_data_error.read(), name=input_data_error.name, content_type='multipart/form-data')

        self.data_ok = {
            'input_file' : input_data_ok
        }
        self.data_error = {
            'input_file' : input_data_error
        }
        
    def test_create_new_report__response_success(self):
        """ Create new report with successful response. """
        request = self.client.post(self.url, self.data_ok)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_create_new_report_without_file__response_error(self):
        """ Create new report without file, error response. """
        request = self.client.post(self.url, {})
        self.assertEqual(request.status_code, status.HTTP_401)

    def test_create_new_report_with_wrong_structure__response_error(self):
        """ Create new report with wrong structure in file, error response. """
        request = self.client.post(self.url, self.data_error)
        self.assertEqual(request.status_code, status.HTTP_401)

