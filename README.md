# Serverless App for image recognition
Simple API for the recognition of images using AWS Rekognition on the back-end. Users for this API are other developers. The API stores an image, does image recognition on it and returns results to the user in two ways, with :
1. A callback. 
2. A GET endpoint.

## Requirements
1. serverless framework Version: 1.83.3
2. npm: 7.7.6
3. node: v15.14.0

## Installation
1. Clone the repo and `cd` to its directory.
2. Run `serverless plugin install -n serverless-apigateway-service-proxy`.
3. Run `sls deploy`

## User Workflow
1. Send request with optionally provided callback_url in request body. Response return unique upload_url.
2. The user uploads a picture to the upload_url
3. Once the image has been PUT to the upload_url, it gets stored in an S3 bucket. Once successfully stored, this will trigger the image recognition process
4. Once the image recognition process finishes, the user receives a callback under the callback_url they indicated in the first step
5. User can also retrieve the results from a GET endpoint

## Test Workflow
 The test_output folder includes image detections for multiple test images.
 #### note
 tests 6 and 7 are showing the output of  
 -  uploading black image (showing example of bad detection), having a Warning message in the returned record, and
 -  uploading .txt file which is not acceptable format for detection. having an Error message in the returned record
