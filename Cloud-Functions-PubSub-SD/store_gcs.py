import base64
import json
from google.cloud import storage

def store_pubsub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    pubsub_message = eval(pubsub_message)
    
    # read the pubsub message and gather essentials
    file_name = pubsub_message['name'] + '.json'
    file_content = eval(pubsub_message['content'])
    gcs_bucket = file_content['destination']

    # Initiate a storage client and a bucket variable
    storage_client = storage.Client()
    bucket = None
    
    # Create a bucket, if one does not exist else, use the existing bucket
    try:
        bucket = storage_client.create_bucket(gcs_bucket)
    except Exception as e:
        bucket = storage_client.get_bucket(gcs_bucket)
        
    # upload the contents to a file in the above bucket
    blob = bucket.blob(file_name)
    blob.upload_from_string(json.dumps(file_content, indent = 4, sort_keys=True))