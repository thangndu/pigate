#! /usr/bin/python
import RPi.GPIO as GPIO
import time
import math
import paho.mqtt.client as mqtt
import io
import sys, errno
import socket

# initialize mqtt publisher
#broker_address="192.168.2.175"

broker_address="iot.eclipse.org"

print("creating new instance")
client = mqtt.Client("distance_pub") #create new instance

print("connecting to broker")
client.connect(broker_address) #connect to broker

print("connected to broker")



TriggerPIN = 16
EchoPIN = 18


# initialize sensors
GPIO.setmode(GPIO.BOARD)
GPIO.setup(TriggerPIN,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(EchoPIN,GPIO.IN)
print ("sensors initializing . . .")

time.sleep(2)

print ("sensors ready")

print ("press ctrl+c to end program")


def checkdist():
    GPIO.output(TriggerPIN, GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(TriggerPIN, GPIO.LOW)
    while not GPIO.input(EchoPIN):
        pass
    t1 = time.time()
    while GPIO.input(EchoPIN):
        pass
    t2 = time.time()
    return (t2-t1)*340/2


present = False

client.loop_start()

try:
    while True:

	d = math.floor(checkdist())

	if (d == 0) and (present == False):
            present = True
            print "car coming"
	    client.publish("camera", "capture")
	elif (d > 0) and (present == True):
	    print "car leaving"
	    client.publish("gate", "close")
	    client.publish("alarm", "turn_off")
 	    present = False

	time.sleep(0.1)


except KeyboardInterrupt:
    GPIO.cleanup() #reset all GPIO
    client.loop_stop()
    print ("Program ended")

