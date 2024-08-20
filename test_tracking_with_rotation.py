import cv2
from utils import select_roi, camshift_tracking

def track_rotating_object(video_path):
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    if not ret:
        print("Failed to read video")
        cap.release()
        return

    roi = select_roi(frame)
    cv2.destroyWindow('Select ROI')

    camshift_tracking(cap, roi)
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    track_rotating_object('rotating_object.avi')
