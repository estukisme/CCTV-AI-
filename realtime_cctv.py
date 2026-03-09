import os
import cv2
import numpy as np
import threading
import tensorflow as tf
from ultralytics import YOLO

# ============================
# 1. Load Model
# ============================

# YOLO deteksi objek
yolo = YOLO("yolov8n.pt")

# CNN grayscale hasil training Kak Jun
cnn = tf.keras.models.load_model("model_cnn_gray.h5")
cnn_labels = ["merah", "tidak_merah"]

print("Hybrid YOLO + CNN Grayscale (FINAL) berjalan...")
print("Tekan Q untuk berhenti.\n")

# ============================
# 2. Alarm Non-blocking (FAST)
# ============================

def alarm():
    threading.Thread(
        target=lambda: os.system(
            "afplay /System/Library/Sounds/Glass.aiff"
        )
    ).start()

# ============================
# 3. Webcam
# ============================

cap = cv2.VideoCapture(0)

# Confidence CNN > 0.80 biar ngga false alarm
CNN_THRESHOLD = 0.80


while True:
    ret, frame = cap.read()
    if not ret:
        print("Kamera gagal membaca frame.")
        break

    # YOLO detect
    results = yolo(frame, stream=True)

    for r in results:
        for box in r.boxes:

            # Bounding box YOLO
            x1, y1, x2, y2 = box.xyxy[0].int().tolist()

            # Crop objek
            crop = frame[y1:y2, x1:x2]
            if crop.size == 0:
                continue

            # ============================
            # CNN Grayscale Predict
            # ============================

            crop_gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

            # Fokus ke tengah (hindari background conveyor baca "tidak_merah")
            h, w = crop_gray.shape
            pad = int(min(h, w) * 0.15)   # ambil 70% bagian tengah
            crop_gray = crop_gray[pad:h-pad, pad:w-pad]

            if crop_gray.size == 0:
                continue

            # Resize
            img64 = cv2.resize(crop_gray, (64, 64), interpolation=cv2.INTER_AREA)

            # Normalisasi
            img_norm = img64.astype("float32") / 255.0

            # Bentuk input CNN
            img_input = img_norm.reshape(1, 64, 64, 1)

            # Prediksi CNN
            pred = cnn.predict(img_input, verbose=0)[0]
            class_id = int(np.argmax(pred))
            confidence = float(np.max(pred))
            color_class = cnn_labels[class_id]

            # ============================
            # 4. Alarm — hanya jika benar-benar tidak merah
            # ============================

            if color_class == "tidak_merah" and confidence >= CNN_THRESHOLD:
                alarm()

            # ============================
            # 5. Render hasil
            # ============================

            label_text = f"{color_class} ({confidence:.2f})"

            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(frame, label_text, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (255, 0, 0), 2)


    cv2.imshow("Realtime Hybrid YOLO + CNN (FINAL)", frame)

    # Stop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
