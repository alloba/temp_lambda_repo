import logging
import os
import urllib3



logger = logging.getLogger(__name__)

def lambda_handler(event, context):
    source_bucket = os.environ.get('SOURCE_BUCKET')
    destination_bucket = os.environ.get('DESTINATION_BUCKET')
    destination_sqs = os.environ.get('DESTINATION_SQS_URL') #TODO -- not needed if using destinations directly
    activity_service_url = os.environ.get('ACTIVITY_SERVICE_URL')

    try:
        if not source_bucket or not destination_bucket:
            raise Exception(f'Missing runtime configuration - source/destination buckets - [{str(source_bucket)} | {str(destination_bucket)}]')
        if not destination_sqs:
            raise Exception('Missing runtime configuration - destination SQS url')
        if not activity_service_url:
            raise Exception(f'Missing runtime configuration - activity_service url')

        #TODO - grab required fields out of the event object, check fields exist

        whatever_this_function_is_called()
    except Exception as e:
        logger.error(f'Operation Failed')
        raise e


def whatever_this_function_is_called():
    # make some API call
    #       http = urllib3.PoolManager()
    #       resp = http.request(
    #           "POST",
    #           "https://httpbin.org/post",
    #           fields={"hello": "world"} #  Add custom form fields
    #       )
    #
    #       resp.json()
    #       resp.status


    # copy from s3 bucket
    # to another s3 bucket
    #           import boto3
    #           s3 = boto3.resource('s3')
    #           copy_source = {
    #               'Bucket': 'amzn-s3-demo-bucket1',
    #               'Key': 'mykey'
    #           }
    #           s3.meta.client.copy(copy_source, 'amzn-s3-demo-bucket2', 'otherkey')


    # send folder event to sqs
    # send file event to sqs
    # TODO -- actually you can just specify destinations in the lambda - https://aws.amazon.com/blogs/compute/introducing-aws-lambda-destinations/
    #
    #       sqs = boto3.client('sqs')
    #       response = sqs.send_message(
    #           QueueUrl=queue_url,
    #           MessageAttributes={
    #               'Title': {
    #                   'DataType': 'String',
    #                   'StringValue': 'The Whistler'
    #               },
    #               'Author': {
    #                   'DataType': 'String',
    #                   'StringValue': 'John Grisham'
    #               },
    #               'WeeksOn': {
    #                   'DataType': 'Number',
    #                   'StringValue': '6'
    #               }
    #           },
    #           MessageBody=(
    #               'Information about current NY Times fiction bestseller for '
    #               'week of 12/11/2016.'
    #           )
    #       )
    #
    #       print(response['MessageId'])
    return 42