# Reference: https://pyimagesearch.com/2014/08/04/opencv-python-color-detection/
import cv2
import numpy as np

# Defining a list of boundaries in the HSV space
# H (hue) defines the position of the color in the range of 0 to 180
# S (saturation) defines the intensity of the color
# V (value) defines the brightness of the color
boundaries = {
    "red": [(0, 100, 100), (10, 255, 255)],        # Lower red
    "red2": [(160, 100, 100), (180, 255, 255)],    # Upper red (wrap-around)
    "blue": [(100, 100, 100), (140, 255, 255)],  # Blue range
    "green": [(40, 100, 100), (90, 255, 255)],     # Green range
    "yellow": [(20, 100, 100), (35, 255, 255)]   # Yellow range
}

# %% Open CV Video Capture and frame analysis
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

# The loop will break on pressing the 'q' key
while True:
    try:
        # Capture one frame
        ret, frame = cap.read()

        # Resize to fit on screen
        target_width = 640
        frame = cv2.resize(frame, (target_width, round(target_width / frame.shape[1] * frame.shape[0])))

        # Convert to HSV for color classification based on hue
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        output = {}

        # loop over the boundaries
        for color, (lower, upper) in boundaries.items():
            # create NumPy arrays from the boundaries
            lower = np.array(lower, dtype="uint8")
            upper = np.array(upper, dtype="uint8")

            # find the colors within the specified boundaries and apply the mask (basically segmenting for colours)
            mask = cv2.inRange(frame, lower, upper)
            output[color] = (cv2.bitwise_and(frame, frame, mask=mask))  # Segmented frames are appended

        # Handle red channel separately due to wrap around
        red_mask1 = cv2.inRange(frame, np.array(boundaries["red"][0]), np.array(boundaries["red"][1]))
        red_mask2 = cv2.inRange(frame, np.array(boundaries["red2"][0]), np.array(boundaries["red2"][1]))
        red_mask = cv2.bitwise_or(red_mask1, red_mask2)
        output["red"] = cv2.bitwise_and(frame, frame, mask=red_mask)

        # Output is appeneded to be of size Pixels X 3 (for R, G, B)
        red_img = output["red"]
        green_img = output["green"]
        blue_img = output["blue"]
        yellow_img = output["yellow"]

        # horizontal Concatination for displaying the images and colour segmentations
        catImg = cv2.hconcat([cv2.vconcat([frame, frame]), cv2.vconcat([red_img, green_img]), cv2.vconcat([blue_img, yellow_img])])

        # Convert back to RGB
        catImg = cv2.cvtColor(catImg, cv2.COLOR_HSV2BGR)

        cv2.imshow("Images with Colours", catImg)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    except KeyboardInterrupt:
        break

cap.release()
cv2.destroyAllWindows()