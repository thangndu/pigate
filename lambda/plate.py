from __future__ import print_function

import json
import urllib
import boto3
import paho.mqtt.client as mqtt

print('Loading function')

s3 = boto3.client('s3')
rk = boto3.client('rekognition')


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # initialize mqtt publisher
    broker_address="iot.eclipse.org"
    client = mqtt.Client("lambda_pub") #create new instance
    client.connect(broker_address) #connect to broker

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key']).decode('utf8')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        img_data = response['Body'].read()
        results = rk.detect_text(Image={'Bytes': img_data})
        textArray = results["TextDetections"]

        if (len(textArray) > 0):
            plate_number = textArray[0]["DetectedText"]
        else:
            plate_number = "XXX-XXX.XX"
        
        client.publish("lambda",plate_number)
        
        return plate_number
        
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
