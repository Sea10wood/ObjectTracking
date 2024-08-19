import cv2
import numpy as np

def select_roi(frame):
    roi = cv2.selectROI(frame, False)
    return roi

def camshift_tracking(cam, roi):
    x, y, w, h = roi
    ret, frame = cam.read()

    if not ret:
        print("Failed to capture frame")
        return

    hsv_roi = cv2.cvtColor(frame[y:y+h, x:x+w], cv2.COLOR_BGR2HSV)
    roi_hist = cv2.calcHist([hsv_roi], [0], None, [180], [0, 180])
    roi_hist = cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

    while True:
        ret, frame = cam.read() 
        if not ret:
            print("Failed to capture frame")
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        back_proj = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)

        ret, roi = cv2.CamShift(back_proj, roi, (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1))

        pts = cv2.boxPoints(ret)
        pts = np.int0(pts)
        frame = cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

        cv2.imshow('Camshift Tracking', frame)
    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

def track_in_webcam():
    cam = cv2.VideoCapture(0)  

    if not cam.isOpened():
        print("Failed to open webcam")
        return

    ret, frame = cam.read()
    if not ret:
        print("Failed to capture image")
        return

    roi = cv2.selectROI('Select ROI', frame, fromCenter=False, showCrosshair=True)
    cv2.destroyWindow('Select ROI')

    if roi[2] <= 0 or roi[3] <= 0:
        print("Invalid ROI selection. Exiting.")
        return

    camshift_tracking(cam, roi)

if __name__ == "__main__":
    track_in_webcam()
