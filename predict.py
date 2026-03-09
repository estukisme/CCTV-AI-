import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import sys

# -------------------------
# Load model
# -------------------------
MODEL_PATH = "my_model.keras"  # atau my_model.h5
model = tf.keras.models.load_model(MODEL_PATH)

# -------------------------
# Load Class Labels
# -------------------------
# Sesuaikan label sesuai training Kak Jun
class_names = ["putih", "merah"]      

# -------------------------
# Fungsi Prediksi
# -------------------------
def predict_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))  # sesuaikan input model
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0]).numpy()

    predicted_class = class_names[np.argmax(score)]
    confidence = np.max(score)

    return predicted_class, confidence


# -------------------------
# CLI Mode
# -------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Cara pakai: python predict.py path_ke_gambar")
        sys.exit()

    file_path = sys.argv[1]
    predicted, conf = predict_image(file_path)

    print("======================================")
    print(f"File       : {file_path}")
    print(f"Prediksi   : {predicted}")
    print(f"Akurasi    : {conf*100:.2f}%")
    print("======================================")
