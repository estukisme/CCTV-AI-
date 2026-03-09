import tensorflow as tf
from tensorflow.keras import layers, models

def build_cnn():
    model = models.Sequential([
        layers.Input(shape=(64, 64, 3)),
        layers.Conv2D(16, (3,3), activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(32, (3,3), activation='relu'),
        layers.MaxPooling2D(),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(3, activation='softmax')  # MERAH, HIJAU, BIRU
    ])
    return model
