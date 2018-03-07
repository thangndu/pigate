from __future__ import print_function

import json
import urllib
import boto3
import paho.mqtt.client as mqtt
import redis
import time

print('Loading function')

s3 = boto3.client('s3')
rk = boto3.client('rekognition')
r = redis.Redis(host='redis-12738.c10.us-east-1-3.ec2.cloud.redislabs.com', port='12738', password='ySiZmGOaqAQroiVp')

plate_number_list = r.lrange('platenumber',0,-1)

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

            new_plate_number = plate_number.replace('-','')
	    new_plate_number = new_plate_number.replace('.','')
	    new_plate_number = new_plate_number.replace(' ','')

            for row in plate_number_list:
                if (new_plate_number == row):
		    access_status = True
                    break
                else:
		    access_status = False
            
        else:
            plate_number = "XXX-XXX.XX"
            access_status = False
            #client.publish("alarm", "turn_on")

        f (access_status == True):
	    client.publish("gate", "open")
	    client.publish("speaker","welcome")
	else:
	    client.publish("alarm", "turn_on")
        
        client.publish("display",plate_number)

        access_time = time.strftime("%A, %d %B %Y %H:%M:%S") 

	#update platenumber into redis
        r.hmset('pigate',{'plate_number':plate_number, 'access_time':access_time, 'access_status':access_status})

        
        return plate_number
        
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
