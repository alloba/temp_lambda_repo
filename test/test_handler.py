import os
import unittest
from unittest.mock import patch, Mock

from src.handler import lambda_handler


class TestHandler(unittest.TestCase):

    def setUp(self):
        os.environ['DESTINATION_BUCKET'] = "some_value"
        os.environ['DESTINATION_SQS_URL'] = "some_value"
        os.environ['ACTIVITY_SERVICE_URL'] = "some_value"

    def test_lambda_handler_missing_runtime_parameter_fails(self):
        os.environ['DESTINATION_BUCKET'] = ""

        with self.assertRaisesRegex(Exception, 'missing runtime parameters'):
            lambda_handler({}, None)

    def test_lambda_handler_missing_object_id_fails(self):
        with self.assertRaisesRegex(Exception, 'field "object_id" not provided in event'):
            lambda_handler({'not_object_id':'asdf'}, None)

    @patch('src.handler.http')
    def test_lambda_handler_failed_activity_service_call(self, mock_http):
        mock_response = Mock()
        mock_response.status = 500
        mock_response.json = Mock(return_value={})
        mock_http.request.return_value = mock_response

        with self.assertRaisesRegex(Exception, ".*status 500.*"):
            lambda_handler({'object_id': 'asdf'}, None)
