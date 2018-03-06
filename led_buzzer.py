#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
import threading
import sys

LedPin = 15
BeepPin = 13

GPIO.setmode(GPIO.BOARD)       # Numbers pins by physical location
GPIO.setup(LedPin, GPIO.OUT)       # Set pin mode as output
GPIO.output(LedPin, GPIO.HIGH)     # Set pin to high(+3.3V) to off the led
GPIO.setup(BeepPin, GPIO.OUT)
GPIO.output(BeepPin, GPIO.LOW)

def Blinking(event):
    event.wait()
    while True:
    	e = event.is_set()
	while (e):
	    GPIO.output(LedPin, GPIO.LOW) #Led on
	    GPIO.output(BeepPin, GPIO.HIGH) #Buzzer on
	    time.sleep(0.5)
	    GPIO.output(LedPin, GPIO.HIGH) #Led off
	    GPIO.output(BeepPin, GPIO.LOW) #Buzzer off
	    time.sleep(0.5)
	    e = event.is_set()
	break

        time.sleep(1)

    thread.run()

event = threading.Event() 
thread  = threading.Thread(target=Blinking, args=(event,))
thread.start()


alarm = False


def on_message(client, userdata, message):
    global event
    m = str(message.payload.decode("utf-8"))
    if (m == "turn_on"):
	event.set()
	print "turn on"

    elif (m == "turn_off"):
	event.clear()
	print "turn off"


broker_address="192.168.2.175"
print("creating new instance")
client = mqtt.Client("led_buzzer_sub") #create new instance
client.on_message=on_message #attach function to callback
print("connecting to broker")
client.connect(broker_address) #connect to broker

print("connected to broker")

print "led ready"

client.loop_start() #start the loop

try:
    while True:
        client.subscribe("alarm")
        time.sleep(0.1) # wait

except KeyboardInterrupt:
    client.loop_stop() #stop the loop
    GPIO.cleanup() # Release resource
    print '\n! Received keyboard interrupt, quitting threads.\n'
    event.set()
