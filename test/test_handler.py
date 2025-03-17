import os
import unittest

from src.handler import whatever_this_function_is_called, lambda_handler


class TestHandler(unittest.TestCase):
    def tearDown(self):
        os.environ['SOURCE_BUCKET'] = ""
        os.environ['DESTINATION_BUCKET'] = ""
        os.environ['DESTINATION_SQS_URL'] = ""
        os.environ['ACTIVITY_SERVICE_URL'] = ""

    def test_lambda_handler_missing_source_bucket_throws(self):
        os.environ['SOURCE_BUCKET'] = ""

        with self.assertRaisesRegex(Exception,'.*buckets'):
            lambda_handler({}, None)

    def test_lambda_handler_missing_destination_sqs_throws(self):
        os.environ['SOURCE_BUCKET'] = "src"
        os.environ['DESTINATION_BUCKET'] = "dest"
        os.environ['DESTINATION_SQS_URL'] = ""

        with self.assertRaisesRegex(Exception,'.*destination SQS url'):
            lambda_handler({}, None)

    def test_lambda_handler_missing_activity_service_key(self):
        os.environ['SOURCE_BUCKET'] = "src"
        os.environ['DESTINATION_BUCKET'] = "dest"
        os.environ['DESTINATION_SQS_URL'] = "sqs"

        with self.assertRaisesRegex(Exception,'.*activity_service url'):
            lambda_handler({}, None)

    def test_whatever_this_function_is_called(self):
        self.assertEqual(42, whatever_this_function_is_called())

