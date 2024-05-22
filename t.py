import torch
import cv2
import datetime
def load_model_and_setup():
    model = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    return model, cap

def process_frame(cap):
    ret, frame = cap.read()
    if not ret:
        return None
    frame = cv2.flip(frame, 1)
    frame_rgb = frame[:, :, ::-1]
    return frame_rgb, frame

def detect_and_track_objects(frame_rgb, model, trackers, frame):
    results = model([frame_rgb]) 
    if len(trackers) == 0:
        for *xyxy, conf, cls in results.xyxy[0]:
            if results.names[int(cls)] == 'person':
                bbox = (int(xyxy[0]), int(xyxy[1]), int(xyxy[2] - xyxy[0]), int(xyxy[3] - xyxy[1]))
                tracker = cv2.TrackerBoosting_create()
                tracker.init(frame, bbox)
                trackers

def update_trackers_and_display(frame, trackers):
    for i, (tracker, old_bbox, start_time) in enumerate(trackers):
        (success, box) = tracker.update(frame)
        if success:
            x, y, w, h = [int(v) for v in box]
            elapsed_time = (datetime.datetime.now() - start_time).total_seconds()
            timer_text = f"{int(elapsed_time // 3600):02}:{int((elapsed_time % 3600) // 60):02}:{int(elapsed_time % 60):02}"
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, timer_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
    cv2.imshow('YOLOv5 Detection', frame)

def main_loop():
    model, cap = load_model_and_setup()
    trackers = []
    while True:
        frame_rgb, frame = process_frame(cap)
        if frame is None:
            break
        detect_and_track_objects(frame_rgb, model, trackers,frame)
        update_trackers_and_display(frame, trackers)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

main_loop()
