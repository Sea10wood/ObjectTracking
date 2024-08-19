import cv2
import numpy as np
from utils import select_roi, camshift_tracking

def track_in_webcam():
    cam = cv2.VideoCapture(1)
    ret, frame = cam.read()
    if not ret:
        print("Failed to capture image")
        cam.release()
        return

    roi = select_roi(frame)
    camshift_tracking(cam, roi)
    cam.release()
    cv2.destroyAllWindows()
