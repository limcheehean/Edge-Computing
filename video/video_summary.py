import cv2
from cv2 import VideoCapture, VideoWriter, VideoWriter_fourcc, CAP_PROP_FPS, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import mediapipe as mp

# Setup detector
base_options = python.BaseOptions(model_asset_path='efficientdet.tflite')
options = vision.ObjectDetectorOptions(base_options=base_options,
                                       score_threshold=0.25)
detector = vision.ObjectDetector.create_from_options(options)

# Extract frames
frames = []
capture = VideoCapture("original.mp4")
fps, width, height = capture.get(CAP_PROP_FPS), int(capture.get(CAP_PROP_FRAME_WIDTH)), int(capture.get(CAP_PROP_FRAME_HEIGHT))
success, frame = capture.read()
while success:
    frames.append(frame)
    success, frame = capture.read()
capture.release()

writer = VideoWriter("summary.avi", VideoWriter_fourcc(*'XVID'), fps, (width, height))

for _, frame in enumerate(frames):
    print(f"\rProcessing frame {_} of {len(frames)}", end="")

    # Perform detection
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
    categories = [category[0].category_name for category in [detection.categories for detection in detector.detect(mp_image).detections]]

    # Save frames with cell phone
    if "cell phone" in categories:
        print("\rCell Phone detected", end="")
        writer.write(frame)

writer.release()

