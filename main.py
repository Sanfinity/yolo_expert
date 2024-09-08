import cv2
import time
from ultralytics import YOLO

# Suppress the verbose logs
import logging
logging.getLogger('ultralytics').setLevel(logging.INFO)

# Load the model
model = YOLO("yolov5xu.pt")

# Open the video file or stream
video_path = "video_src/sample.mp4"
cap = cv2.VideoCapture(video_path)

width = 1280
height = 720

# Get the video's original frame rate
fps = cap.get(cv2.CAP_PROP_FPS)
frame_duration = 1 / fps

while cap.isOpened():
    success, frame = cap.read()

    if success:
        frame = cv2.resize(frame, (width, height))
        start_time = time.time()

        # Perform tracking
        results = model.track(frame, persist=True, conf=0.5, iou=0.3, tracker="bytetrack.yaml")
        annotated_frame = results[0].plot()

        # Get detection metrics
        num_detections = len(results[0].boxes)
        elapsed_time = time.time() - start_time
        fps_display = 1 / elapsed_time

        # Overlay detection metrics on the frame
        cv2.putText(annotated_frame, f"FPS: {fps_display:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(annotated_frame, f"Detections: {num_detections}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display the annotated frame
        cv2.imshow("YOLOv9 Tracking", annotated_frame)

        # Print detection metrics to the command window
        logging.debug(f"FPS: {fps_display:.2f}, Detections: {num_detections}")

        # Wait for the appropriate amount of time
        wait_time = max(1, int((frame_duration - elapsed_time) * 1000))
        if cv2.waitKey(wait_time) & 0xFF == ord("q"):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
