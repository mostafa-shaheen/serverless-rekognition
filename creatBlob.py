import json
import boto3
import time
import os

table_name = os.environ.get("ENV_TABLE_NAME")
bucket_name = os.environ.get("ENV_TABLE_NAME")

def handler(event, context):
    s3 = boto3.client("s3")
    table = boto3.resource('dynamodb').Table(table_name)
    
    
    object_id = time.strftime('%Y_%m_%d_%H_%M_%S', time.gmtime())

    if event['multiValueQueryStringParameters']:
        callback= event['multiValueQueryStringParameters']['callback-url']
        table.put_item(Item={'ID': object_id, 'callback_url': callback[0]})
    else:
        table.put_item(Item={'ID': object_id})
        
    URL = s3.generate_presigned_url("put_object", Params={"Bucket": bucket_name, "Key": object_id}, ExpiresIn=180 )

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"URL": URL, "object_id": object_id})
    }
