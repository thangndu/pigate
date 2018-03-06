#! /usr/bin/python
import time
import paho.mqtt.client as mqtt
import io
import picamera
import boto3

def on_message(client, userdata, message):
    m = str(message.payload.decode("utf-8"))
    print m
    if m == "capture":
    	time.sleep(1)
        plate_capture()


# initialize mqtt publisher
#broker_address="192.168.2.175"
broker_address="iot.eclipse.org"

print("creating new instance")
client = mqtt.Client("camera_sub") #create new instance
client.on_message=on_message #attach function to callback
print("connecting to broker")
client.connect(broker_address) #connect to broker

print("connected to broker")


# initialize camera
camera = picamera.PiCamera()
camera.resolution = (320,240)
print "camera initializing ..."
#camera warm-up time
time.sleep(2)
print "camera ready"

print ("press ctrl+c to end program")


s3 = boto3.resource('s3', aws_access_key_id='xxxxx', aws_secret_access_key='xxxxx', region_name='us-west-2')
bucket_name = 'platenumber'
object_name = 'platenumber.jpg'
bucket = s3.Bucket(bucket_name) 
stream = io.BytesIO()


def plate_capture():

    camera.capture(stream, format='jpeg', use_video_port=True)

    stream.seek(0)
    print "uploading image to S3"
    bucket.put_object(Key=object_name, Body=stream.read())
    #image = s3.Object(bucket, photo)
    object = bucket.Object(object_name) 
    object.Acl().put(ACL='public-read')
    print "completed"
    stream.seek(0)
    stream.truncate()


client.loop_start() #start the loop

try:
    while True:
        client.subscribe("camera")
        time.sleep(0.1) # wait

except KeyboardInterrupt:
    client.loop_stop() #stop the loop
    stream.close()


