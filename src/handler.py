import logging
import os
import urllib3
import boto3
import json

from src.models import FileAttachment, FileUploadEvent

logger = logging.getLogger(__name__)
http = urllib3.PoolManager()
s3 = boto3.resource('s3')
sqs = boto3.client('sqs')


def lambda_handler(event, context):
    destination_bucket = os.environ.get('DESTINATION_BUCKET')
    destination_sqs = os.environ.get('DESTINATION_SQS_URL')
    activity_service_url = os.environ.get('ACTIVITY_SERVICE_URL')

    try:
        if not destination_bucket or not destination_sqs or not activity_service_url:
            raise Exception('missing runtime parameters')

        document_uuid = event.get('object_id')
        if not document_uuid:
            raise Exception('field "object_id" not provided in event')

        logger.info(f'beginning operation for uuid: {document_uuid}')
        #TODO - i feel like we're supposed to process the incoming file itself, as well? yes/no?
        #       not sure where you would want to copy it to though, in s3.
        process_uuid_attachments(document_uuid, activity_service_url, destination_bucket, destination_sqs)

    except Exception as e:
        logger.error(f'Operation Failed')
        raise e

def process_uuid_attachments(uuid: str, activity_service_url: str, destination_bucket: str, destination_sqs: str):
    resp = http.request('GET',f'{activity_service_url}/{uuid}')

    if resp.status != 200:
        raise Exception(f'status {resp.status} from {activity_service_url} for object_id {uuid}')

    attachment_data = resp.json()

    for attachment_raw in attachment_data:
        attachment = FileAttachment(**attachment_raw)
        attachment_data_request = http.request(method='GET', url=attachment.privateAttachment)
        if attachment_data_request.status != 200:
            raise Exception(f'failed to download attachment for {uuid} : {attachment.name}')

        s3.upload_fileobj(attachment_data_request.data, destination_bucket, attachment.filePath) #TODO - not sure if filepath is correct

        sqs_message = FileUploadEvent()
        #TODO - it feels like there should be more entries here, but i don't know what they are supposed to be.
        #       there's data keys that i don't know how to fill in the example json (file_upload_event.json).
        sqs_message.data = [(
            #TODO - some implied additional dicts also go here?
            {
            "name": "files",
            "key": False,
            "files": [{
                "s3_key": attachment.filePath,
                "display_name":attachment.name,
                "s3_bucket": destination_bucket,
                "document_type":"" #TODO - how would i know this.
            }]
        })]
        sqs.send_message(QueueUrl=destination_sqs, MessageBody=json.dumps(sqs_message))