import i2c_lcd1602 as lcd
import os
import paho.mqtt.client as mqtt
import time


screen = lcd.Screen(bus=1, addr=0x3f, cols=16, rows=2)
time.sleep(1)
text = "                "
screen.enable_backlight()
screen.display_data(text)


def on_message(client, userdata, message):
    global screen
    m = str(message.payload.decode("utf-8"))
    screen.display_data(m)
    print m

#broker_address="192.168.2.175"
broker_address="iot.eclipse.org"

print("creating new instance")
client = mqtt.Client("display_sub") #create new instance
client.on_message=on_message #attach function to callback
print("connecting to broker")
client.connect(broker_address) #connect to broker

print("connected to broker")

client.loop_start() #start the loop

try:
    while True:
    	client.subscribe("display")
    	time.sleep(0.1) # wait

except KeyboardInterrupt:
 
    client.loop_stop() #stop the loop

