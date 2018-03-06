#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt

def setServoAngel(angel):
    print angel, " degree..."
    duty = angel / 18 + 2.5
    p.ChangeDutyCycle(duty)
    time.sleep(1)


servoControlPin=36

GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
GPIO.setup(servoControlPin, GPIO.OUT)
p = GPIO.PWM(servoControlPin, 50)
p.start(0)


def on_message(client, userdata, message):
    m = str(message.payload.decode("utf-8"))
    print m

    if (m == "open"):
    	setServoAngel(90) #open gate
    elif (m == "close"):
        setServoAngel(0) #open gate



broker_address="iot.eclipse.org"
#broker_address="192.168.2.175"

print("creating new instance")
client = mqtt.Client("gate_sub") #create new instance
client.on_message=on_message #attach function to callback
print("connecting to broker")
client.connect(broker_address) #connect to broker

print("connected to broker")

print "gate ready"


client.loop_start() #start the loop

try:
    while True:
    	client.subscribe("gate")
    	time.sleep(0.1) # wait

except KeyboardInterrupt:
    client.loop_stop() #stop the loop
    p.stop()
    GPIO.cleanup() # Release resource
	



