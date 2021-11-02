import json
import botocore.vendored.requests as requests

def handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    new_image = event['Records'][0]['dynamodb']['NewImage'] # new image of an item that was updated in dynamodb either with put_item or update_item
    
    labels_recorded = 'Labels' in new_image
    callback_url_exist = 'callback_url' in new_image
    
    if labels_recorded and callback_url_exist:
        labels =  new_image['Labels']
        callback_url =  new_image['callback_url']
        response = requests.post(callback_url, data = labels) 
    return 'Successfully processed {} records.'.format(len(event['Records']))
