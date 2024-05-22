import torch
import datetime
import cv2

# Load the YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True)

# Open a handle to the default webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Set the desired frame width and height
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Dictionary to track the start times and durations of detected persons
detection_start_times = {}

# Read frames from the webcam in a loop
while True:
    ret, frame = cap.read()
    if not ret:
        break  # Exit the loop if no more frames or error

    # Flip the frame horizontally (remove mirroring effect)
    frame = cv2.flip(frame, 1)

    # Convert BGR to RGB (YOLOv5 uses RGB)
    frame_rgb = frame[:, :, ::-1]

    # Run inference
    results = model([frame_rgb])

    current_detected = set()

    # Process detection results and display timers
    for *xyxy, conf, cls in results.xyxy[0]:
        label = results.names[int(cls)]
        if label == 'person':
            # Calculate the center of the bounding box and use it as a unique ID for tracking
            id = ((xyxy[0] + xyxy[2]) // 2, (xyxy[1] + xyxy[3]) // 2)
            current_detected.add(id)
            if id not in detection_start_times:
                detection_start_times[id] = datetime.datetime.now()

            # Calculate the elapsed time in seconds
            elapsed_time = (datetime.datetime.now() - detection_start_times[id]).total_seconds()
            timer_text = f"{int(elapsed_time // 3600):02}:{int((elapsed_time % 3600) // 60):02}:{int(elapsed_time % 60):02}"
            
            # Display the timer on the frame
            cv2.putText(frame, timer_text, (int(xyxy[0]), int(xyxy[1]) - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

            # Draw bounding box and label
            cv2.rectangle(frame, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), (255, 0, 0), 2)
            cv2.putText(frame, label, (int(xyxy[0]), int(xyxy[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # Cleanup: Remove detection times for persons no longer detected
    for id in list(detection_start_times.keys()):
        if id not in current_detected:
            del detection_start_times[id]

    # Display the frame
    cv2.imshow('YOLOv5 Detection', frame)

    # Press 'q' to quit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()