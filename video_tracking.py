import cv2
import numpy as np
from utils import select_roi, camshift_tracking

def track_in_video(video_path):
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    if not ret:
        print("Failed to read video")
        cap.release()
        return

    roi = select_roi(frame)

    camshift_tracking(cap, roi)

    cap.release()
    cv2.destroyAllWindows()

def camshift_tracking(cap, roi):
    x, y, w, h = roi
    ret, frame = cap.read()

    if not ret:
        print("Failed to capture frame")
        return

    hsv_roi = cv2.cvtColor(frame[y:y+h, x:x+w], cv2.COLOR_BGR2HSV)
    roi_hist = cv2.calcHist([hsv_roi], [0], None, [180], [0, 180])
    roi_hist = cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

    while True:
        ret, frame = cap.read()  
        if not ret:
            print("End of video or failed to capture frame")
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        back_proj = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)

        ret, roi = cv2.CamShift(back_proj, roi, (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1))

        pts = cv2.boxPoints(ret)
        pts = np.int0(pts)
        frame = cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

        cv2.imshow('Camshift Tracking', frame)

        if cv2.waitKey(30) & 0xFF == ord('q'):  
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    video_path = "your_video_file_path.avi"  
    track_in_video(video_path)
