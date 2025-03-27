import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
from cv2 import VideoCapture, imencode


def on_message(client_, userdata, message):
    print("Received request to capture image")

    print("Capturing image...")
    capture = VideoCapture(0)
    success, frame = capture.read()
    if not success:
        print("Failed to capture image")
        return
    print("Image captured")

    print("Publishing image...")
    _, buffer = imencode(".png", frame)
    data = buffer.tobytes()
    client.publish("camera/image", data)
    print("Image published")


print("Ready to capture images")
client = mqtt.Client(CallbackAPIVersion.VERSION2)
client.on_message = on_message
client.connect("192.168.1.10", 1883)
client.subscribe("camera/capture")
client.loop_forever()
