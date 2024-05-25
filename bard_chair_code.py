import torch
import datetime
import cv2

# Load the YOLOv5 model for chair detection
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Open a handle to the default webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Set the desired frame width and height
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Read frames from the webcam in a loop
while True:
    ret, frame = cap.read()
    if not ret:
        break # Exit the loop if no more frames or error

    # Flip the frame horizontally (remove mirroring effect)
    frame = cv2.flip(frame, 1)

    # Convert BGR to RGB (YOLOv5 uses RGB)
    frame_rgb = frame[:, :, ::-1]

    # Run inference
    results = model([frame_rgb])

    # Process detection results and display chair coordinates
    for *xyxy, conf, cls in results.xyxy[0]:
        label = results.names[int(cls)]
        if label == 'chair':
            # Calculate the center of the bounding box
            center = ((xyxy[0] + xyxy[2]) // 2, (xyxy[1] + xyxy[3]) // 2)

            # Display chair coordinates on the frame
            cv2.putText(frame, f"Chair: ({int(center[0])}, {int(center[1])})", (int(xyxy[0]), int(xyxy[1]) - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Draw bounding box for the chair
            cv2.rectangle(frame, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('YOLOv5 Chair Detection', frame)

    # Press 'q' to quit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()