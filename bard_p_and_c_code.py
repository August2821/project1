import torch
import datetime
import cv2

# Load YOLOv5 models for person and chair detection
model_person = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True)
model_chair = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Open a handle to the default webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Set the desired frame width and height
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Dictionaries to track start times and IDs for detected persons and chairs
person_start_times = {}
chair_start_times = {}
next_person_id = 0
next_chair_id = 0

# Read frames from the webcam in a loop
while True:
    ret, frame = cap.read()
    if not ret:
        break  # Exit the loop if no more frames or error

    # Flip the frame horizontally (remove mirroring effect)
    frame = cv2.flip(frame, 1)

    # Convert BGR to RGB (YOLOv5 uses RGB)
    frame_rgb = frame[:, :, ::-1]

    # Run inference for person detection
    person_results = model_person([frame_rgb])

    # Run inference for person detection
    results = model_person([frame_rgb]) 

    # Process person detection results and display timers and coordinates
    for *xyxy, conf, cls in person_results.xyxy[0]:
        label = results.names[int(cls)]
        if label == 'person':
            # Calculate the center of the bounding box and use it as a unique ID for tracking
            person_id = ((xyxy[0] + xyxy[2]) // 2, (xyxy[1] + xyxy[3]) // 2)

            # Check if the person is already being tracked
            if person_id in person_start_times:
                # Update the start time if the person is matched
                person_start_times[person_id] = datetime.datetime.now()
            else:
                # Assign a new ID and start time if the person is new
                person_start_times[person_id] = datetime.datetime.now()
                next_person_id += 1

            # Calculate the elapsed time in seconds
            # elapsed_time = (datetime.datetime.now() - person_start_times[person_id]).total_seconds()
            # timer_text = f"{int(elapsed_time // 3600):02}:{int((elapsed_time % 3600) // 60):02}:{int(elapsed_time % 60):02}"

            # Display the timer and coordinates on the frame
            cv2.putText(frame, f"Person: ({int(person_id[0])}, {int(person_id[1])})", (int(xyxy[0]), int(xyxy[1]) - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            # Draw bounding box for the person
            cv2.rectangle(frame, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), (255, 0, 0), 2)

    # Run inference for chair detection
    chair_results = model_chair([frame_rgb])

    # Process chair detection results and display coordinates
    for *xyxy, conf, cls in chair_results.xyxy[0]:
        label = results.names[int(cls)]
        if label == 'chair':
            # Calculate the center of the bounding box
            chair_center = ((xyxy[0] + xyxy[2]) // 2, (xyxy[1] + xyxy[3]) // 2)

            # Display chair coordinates on the frame
            cv2.putText(frame, f"Chair: ({int(chair_center[0])}, {int(chair_center[1])})", (int(xyxy[0]), int(xyxy[1]) - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Draw bounding box for the chair
            cv2.rectangle(frame, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('YOLOv5 Person and Chair Detection', frame)

    # Press 'q' to quit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()