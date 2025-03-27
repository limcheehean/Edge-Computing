import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
from time import time
from os import makedirs
import numpy as np
from cv2 import imdecode, IMREAD_COLOR, imshow, waitKey, imread


def on_message(client, userdata, message):
    filename = f"images/{int(time())}.png"

    print(f"\n\nImage received, saving to file...")
    with open(filename, "wb") as file:
        file.write(message.payload)
    print(f"File saved as {filename}")

    imshow("Received Image", imread(filename))
    waitKey(0)

    # Rewrite input prompt in console
    print("\nPress enter to trigger an image capture: ")
    while True:
        pass


# Create folder to store images
makedirs("images", exist_ok=True)

# Setup mqtt
client = mqtt.Client(CallbackAPIVersion.VERSION2)
client.on_message = on_message
client.connect("192.168.1.10", 1883)
client.subscribe("camera/image")
client.loop_start()

# Send capture request on pressing enter
while True:
    input("Press enter to trigger an image capture: ")
    print("Requesting to capture image...")
    client.publish("camera/capture")
    print("Image capture requested\n")
