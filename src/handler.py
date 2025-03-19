import logging
import os
import urllib3
import boto3
import json

logger = logging.getLogger(__name__)
http = urllib3.PoolManager()
s3 = boto3.resource('s3')
sqs = boto3.client('sqs')


# TODO - The do they have a shared schema they want to work with, other than "here's an example json?"
# TODO - are we supposed to be handling the infrastructure piece as well? that's a whole other thing. (CF/TF/Pulumi/???, IAM standards, CW logging standards, etc.)
# TODO - while lambda destinations would work, i think it's probably not worth bothering with unless the team is already using them.
#        it more directly forces an output format (which i'm sure they arent using), and becomes more difficult to test functionality directly (cannot test downstream effects via web console execution)
#        i'll run it by andrew, but once the conversation is over i assume we'll just be boto-ing the sqs stuff. which isnt bad.
def lambda_handler(event, context):
    source_bucket = os.environ.get('SOURCE_BUCKET')
    destination_bucket = os.environ.get('DESTINATION_BUCKET')
    destination_sqs = os.environ.get('DESTINATION_SQS_URL')
    activity_service_url = os.environ.get('ACTIVITY_SERVICE_URL')

    try:
        if not source_bucket or not destination_bucket or not destination_sqs or not activity_service_url:
            raise Exception('missing runtime parameters')

        document_uuid = event.get('uuid')
        if not document_uuid:
            raise Exception('field "uuid" not provided in event')

        logger.info(f'beginning operation for uuid: {document_uuid}')
        attachment_data = process_uuid_attachments(document_uuid, activity_service_url, source_bucket, destination_bucket)
        send_sqs_updates(document_uuid, attachment_data, destination_sqs)

    except Exception as e:
        logger.error(f'Operation Failed')
        raise e


def process_uuid_attachments(uuid: str, activity_service_url: str, source_bucket: str, destination_bucket: str) -> object:
    resp = http.request(
        'GET',
        f'{activity_service_url}/{uuid}',
    )

    if resp.status != 200:
        raise Exception(f'status {resp.status} from {activity_service_url} for uuid {uuid}')

    attachment_data = resp.json()

    # TODO - not sure what i'm meant to actually be pulling from this API that would allow me to copy stuff
    if not attachment_data.get('folder'):
        raise Exception(f'missing attachment data for uuid {uuid}')

    copy_source = {
        'Bucket': source_bucket,
        'Key': 'mykey' #TODO
    }

    s3.meta.client.copy(copy_source, destination_bucket, 'some_key_here') #TODO

    return attachment_data #TODO : what data is actually needed to form a final sqs message later?


def send_sqs_updates(document_uuid: str, attachment_data: object, destination_sqs: str) -> tuple[dict, dict]:
    # TODO - need to verify basically everything about the expected output
    file_upload_message = {} #TODO
    folder_created_message = {} #TODO

    sqs.send_message(
        QueueUrl=destination_sqs,
        MessageAttributes={},
        MessageBody=json.dumps(folder_created_message)
    )
    sqs.send_message(
        QueueUrl=destination_sqs,
        MessageAttributes={},
        MessageBody=json.dumps(file_upload_message)
    )

    return file_upload_message, folder_created_message
