from video_tracking import track_in_video
from webcam_tracking import track_in_webcam
import cv2
import numpy as np

def create_rotating_video(output_file, num_frames=360):
    width, height = 640, 480
    center = (width // 2, height // 2)
    size = (100, 50)
    angle_step = 360 / num_frames

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_file, fourcc, 20.0, (width, height))

    for i in range(num_frames):
        angle = i * angle_step
        frame = np.zeros((height, width, 3), dtype=np.uint8)

        rect = cv2.boxPoints(((center[0], center[1]), size, angle))
        rect = np.int0(rect)
        cv2.polylines(frame, [rect], isClosed=True, color=(0, 255, 0), thickness=2)

        out.write(frame)

    out.release()
    cv2.destroyAllWindows()

def main():
    mode = input("Choose mode (1: Video File, 2: Webcam, 3: Generate Rotating Video): ")
    if mode == "1":
        track_in_video('videos/flower.mp4')
    elif mode == "2":
        track_in_webcam()
    elif mode == "3":
        output_file = 'videos/rotating_object.avi'
        create_rotating_video(output_file)
        print(f"Rotating object video created: {output_file}")
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
