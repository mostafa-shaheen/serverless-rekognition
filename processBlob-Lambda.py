import boto3
from decimal import Decimal
import json
import urllib.request
import urllib.parse
import urllib.error


print('Loading function')
confidence_threshold = 90

rekognition = boto3.client('rekognition')

# --------------- Helper Functions to call Rekognition APIs ------------------

def detect_labels(bucket, key):
    
    table = boto3.resource('dynamodb').Table('BlobsTableV1')
    
    try:

        response = rekognition.detect_labels(Image={"S3Object": {"Bucket": bucket, "Name": key}})
        labels = [{'Confidence': Decimal(str(label_prediction['Confidence'])), 'Name': label_prediction['Name']} for label_prediction in response['Labels']]
        table.update_item(
                Key={
                    'ID': key,
                },
                UpdateExpression="set Labels=:l",
                ExpressionAttributeValues={
                    ':l': labels
                },
            )
            
        scores = [label_prediction['Confidence'] for label_prediction in response['Labels']]
        if max(scores) < confidence_threshold:
            table.update_item(
                    Key={
                        'ID': key,
                    },
                    UpdateExpression="set Warning_message=:w",
                    ExpressionAttributeValues={
                        ':w': 'Maybe contains bad results (low confidence in detection)'
                    },
                )

        return response
    except Exception as e:
    
        table.update_item(
                Key={
                    'ID': key,
                },
                UpdateExpression="set Error_message=:eVal",
                ExpressionAttributeValues={
                    ':eVal': str(e)
                },
                #ReturnValues="UPDATED_NEW"
            )
    
    
        return str(e)
    

# --------------- Main handler ------------------

def handler(event, context):
    '''Demonstrates S3 trigger that uses
    Rekognition APIs to detect faces, labels and index faces in S3 Object.
    '''
    # Get the object from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    try:

        # Calls rekognition DetectLabels API to detect labels in S3 object
        response = detect_labels(bucket, key)

        # Print response to console.
        print(response)

        return response
    except Exception as e:

        print("Error processing object {} from bucket {}. ".format(key, bucket) +
              "Make sure your object and bucket exist and your bucket is in the same region as this function.")
        raise e
