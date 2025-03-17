import logging
import os
import urllib3

logger = logging.getLogger(__name__)
http = urllib3.PoolManager()

def lambda_handler(event, context):
    source_bucket = os.environ.get('SOURCE_BUCKET')
    destination_bucket = os.environ.get('DESTINATION_BUCKET')
    destination_sqs = os.environ.get('DESTINATION_SQS_URL')  # TODO -- not needed if using destinations directly
    activity_service_url = os.environ.get('ACTIVITY_SERVICE_URL')

    try:
        if not source_bucket or not destination_bucket:
            raise Exception(f'Missing runtime configuration - source/destination buckets - [{str(source_bucket)} | {str(destination_bucket)}]')
        if not destination_sqs: #TODO probably not needed
            raise Exception('Missing runtime configuration - destination SQS url')
        if not activity_service_url:
            raise Exception(f'Missing runtime configuration - activity_service url')

        if not event.get('uuid'):
            raise Exception('field "uuid" not provided in event')

        attachment_data = process_uuid_attachments(event.get('uuid'), activity_service_url)
        form_response(event.get('uuid'), attachment_data)

    except Exception as e:
        logger.error(f'Operation Failed')
        raise e

def process_uuid_attachments(uuid:str, activity_service_url: str) -> object:
    resp = http.request(
        'GET',
        f'activity_service_url/{uuid}',
    )

    if resp.status != 200:
        raise Exception(f'status {resp.status} from {activity_service_url} for uuid {uuid}')

    attachment_data = resp.json()
    if not attachment_data.get('???'):
        raise Exception(f'missing attachment data for uuid {uuid}')

    # TODO - iterate through results and foreach perform copy?
    #        this part needs clarification from andrew
    #        in terms of concrete example responses and specifically how this api interacts with the actual attachments

    # for x in attachment_data:
    #   copy_files_between_s3_buckets(x)
    #                            import boto3
    #                            s3 = boto3.resource('s3')
    #                            copy_source = {
    #                                'Bucket': 'amzn-s3-demo-bucket1',
    #                                'Key': 'mykey'
    #                            }
    #                            s3.meta.client.copy(copy_source, 'amzn-s3-demo-bucket2', 'otherkey')
    #
    #
    # return /maybe the attachment data object?/

def form_response(document_uuid: str, attachment_data: object) -> dict:
    # TODO - need to talk about expectations around how results are being communicated for the lambda
    #        use of destinations vs boto sqs messages, plus working examples to test with/hard confirmation on message shape



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
