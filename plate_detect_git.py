import boto3  
import json
import os
import paho.mqtt.client as mqtt
import time
import io
import redis



def on_message(client, userdata, message):
    m = str(message.payload.decode("utf-8"))

    print m
    
    plate_number = m
	
    new_plate_number = plate_number.replace('-','')
    new_plate_number = new_plate_number.replace('.','')
    new_plate_number = new_plate_number.replace(' ','')

    for row in plate_number_list:
        if (new_plate_number == row):
	    access_status = True
            break
        else:
	    access_status = False
	            
    if (access_status == True):
	client.publish("gate", "open")
	client.publish("speaker","welcome")
    else:
	client.publish("alarm", "turn_on")


    client.publish("display",plate_number)

    access_time = time.strftime("%A, %d %B %Y %H:%M:%S") 

    #update platenumber into redis
    r.hmset('pigate',{'plate_number':plate_number, 'access_time':access_time, 'access_status':access_status})



#subcribe for receive msg from AWS
broker_address="iot.eclipse.org"
print("creating new instance")
client = mqtt.Client("lambda_sub") #create new instance
client.on_message=on_message #attach function to callback
print("connecting to broker")
client.connect(broker_address) #connect to broker

print("connected to broker")


r = redis.Redis(host='xxxxx', port='12738', password='xxxxx')

plate_number_list = r.lrange('platenumber',0,-1)


client.loop_start() #start the loop

try:
    while True:
    	client.subscribe("lambda")
    	time.sleep(0.1) # wait
except KeyboardInterrupt:
    client.loop_stop() #stop the loop


