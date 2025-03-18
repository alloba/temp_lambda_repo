import os
import unittest
from unittest.mock import patch, Mock

from src.handler import lambda_handler


class TestHandler(unittest.TestCase):

    def setUp(self):
        os.environ['SOURCE_BUCKET'] = "some_value"
        os.environ['DESTINATION_BUCKET'] = "some_value"
        os.environ['DESTINATION_SQS_URL'] = "some_value"
        os.environ['ACTIVITY_SERVICE_URL'] = "some_value"

    def test_lambda_handler_missing_source_bucket_throws(self):
        os.environ['SOURCE_BUCKET'] = ""

        with self.assertRaisesRegex(Exception, '.*buckets'):
            lambda_handler({}, None)

    def test_lambda_handler_missing_destination_sqs_throws(self):
        os.environ['DESTINATION_SQS_URL'] = ""

        with self.assertRaisesRegex(Exception, '.*destination SQS url'):
            lambda_handler({}, None)

    def test_lambda_handler_missing_activity_service_key(self):
        os.environ['ACTIVITY_SERVICE_URL'] = ""

        with self.assertRaisesRegex(Exception, '.*activity_service url'):
            lambda_handler({}, None)

    @patch('src.handler.http')
    def test_lambda_handler_failed_activity_service_call(self, mock_http):
        mock_response = Mock()
        mock_response.status = 200
        mock_response.json = Mock(return_value={'status': 'OK'})
        mock_http.request.return_value = mock_response

        with self.assertRaisesRegex(Exception, ".*missing attachment.*"):
            lambda_handler({'uuid': 'asdf'}, None)
