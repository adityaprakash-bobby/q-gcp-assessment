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
    
    storage_client = storage.Client()
    bucket = storage_client.get_bucket('gcpbucketaditya')
    
    file_name = pubsub_message['name'] + '.json'
    file_content = eval(pubsub_message['content'])
	

    blob = bucket.blob(file_name)
    blob.upload_from_string(json.dumps(file_content, indent = 4, sort_keys=True))