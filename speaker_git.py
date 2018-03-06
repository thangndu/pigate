import boto3
import os
import time
import paho.mqtt.client as mqtt


def on_message(client, userdata, message):
    m = str(message.payload.decode("utf-8"))
    print m
    os.system("omxplayer welcome.mp3")


#broker_address="192.168.2.175"
broker_address="iot.eclipse.org"

print("creating new instance")
client = mqtt.Client("speaker_sub") #create new instance
client.on_message=on_message #attach function to callback
print("connecting to broker")
client.connect(broker_address) #connect to broker

print("connected to broker")

client.loop_start() #start the loop

welcome_note = "Welcome home"

polly = boto3.client('polly', aws_access_key_id='xxxxx', aws_secret_access_key='xxxxxx', region_name='us-west-2')

response = polly.synthesize_speech(
    OutputFormat='mp3',
    Text=welcome_note,
    TextType='text',
    VoiceId='Joanna')

with open('welcome.mp3', 'wb') as f:
    f.write(response['AudioStream'].read())

#os.system("omxplayer welcome.mp3")

try:
    while True:
        client.subscribe("speaker")
        time.sleep(0.1) # wait

except KeyboardInterrupt:

    client.loop_stop() #stop the loop

