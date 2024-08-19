from video_tracking import track_in_video
from webcam_tracking import track_in_webcam

def main():
    mode = input("Choose mode (1: Video File, 2: Webcam): ")
    if mode == "1":
        track_in_video('videos/flower.mp4')
    elif mode == "2":
        track_in_webcam()
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
