from ultralytics import YOLO

try:
    model = YOLO("yolov8n.pt")
    print("YOLO OK, model loaded")
except Exception as e:
    print("YOLO ERROR:", e)
