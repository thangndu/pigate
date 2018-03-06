#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt

# initialize mqtt publisher
#broker_address="192.168.2.175"

broker_address="iot.eclipse.org"

print("creating new instance")
client = mqtt.Client("button_pub") #create new instance

print("connecting to broker")
client.connect(broker_address) #connect to broker
print("connected to broker")



BtnPin = 11    # pin11 --- button


GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)
print "button ready"

pressed = False
close = True

client.loop_start()

try:
    while True:

    	if (GPIO.input(BtnPin) == GPIO.LOW):
	    if (pressed == False): # Check whether the button is pressed or not 
	    	pressed = True
	    	print "pressed"

		client.publish("alarm", "turn_off") #turn off alarm
                if (close == True):
		    close = False
		    client.publish("gate", "open")
                else:
		    close = True
		    client.publish("gate", "close")
	    else:
	    	pass
    	else:
	    pressed = False

    	time.sleep(0.1)


except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
    GPIO.cleanup()  # Release resource
    client.loop_stop()

