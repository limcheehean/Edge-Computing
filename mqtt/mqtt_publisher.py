import paho.mqtt.client as mqtt
import time

client = mqtt.Client()
client.connect("192.168.1.10", 1883)

while True:
    client.publish("test/topic", "Hello, MQTT!")
    time.sleep(5)