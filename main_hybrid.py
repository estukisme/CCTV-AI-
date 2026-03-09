import cv2
import numpy as np
from ultralytics import YOLO
from tensorflow.keras.models import load_model

# ================== LOAD MODEL ==================
yolo_model = YOLO("yolo/yolov8n.pt")
cnn_model = load_model("cnn/model_cnn_red.h5")

labels = ["non_merah", "merah"]

# ================== OPEN CAM ==================
cap = cv2.VideoCapture(0)  # ganti 1 atau 2 kalau pakai USB capture card

if not cap.isOpened():
    print("Kamera / capture card tidak terbaca!")
    exit()

print("Hybrid YOLO + CNN berjalan... Tekan Q untuk keluar.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Gagal baca frame!")
        break

    # ================== YOLO DETECTION ==================
    results = yolo_model(frame)[0]

    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        conf = float(box.conf[0])

        # ambil object area
        roi = frame[y1:y2, x1:x2]

        if roi.size == 0:
            continue

        # ================== CNN COLOR CHECK ==================
        img = cv2.resize(roi, (64, 64))
        img = img.astype("float32") / 255.
        img = np.expand_dims(img, axis=0)

        pred = cnn_model.predict(img)[0]
        idx = np.argmax(pred)
        color_label = labels[idx]

        # ================== TAMPILKAN ==================
        color = (0, 255, 0) if color_label == "merah" else (0, 0, 255)

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, f"{color_label} ({conf:.2f})", 
                    (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, color, 2)

    cv2.imshow("Hybrid YOLO + CNN - Kak Jun", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
