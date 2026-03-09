import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

# ============================
# CONFIG
# ============================
IMG_SIZE = 64
BATCH = 32
EPOCHS = 25

train_dir = "../dataset_split/train"
val_dir = "../dataset_split/val"

print("TensorFlow Version:", tf.__version__)

# ============================
# DATASET
# ============================
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=10,
    width_shift_range=0.1,
    height_shift_range=0.1,
    brightness_range=[0.7, 1.3],
    zoom_range=0.1,
    shear_range=0.1,
    horizontal_flip=True
)

val_datagen = ImageDataGenerator(rescale=1./255)

train_gen = train_datagen.flow_from_directory(
    train_dir,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH,
    class_mode='categorical'
)

val_gen = val_datagen.flow_from_directory(
    val_dir,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH,
    class_mode='categorical'
)

# ============================
# BUILD MODEL CNN (MODERN TF)
# ============================
def build_cnn():
    model = models.Sequential([
        layers.Input(shape=(IMG_SIZE, IMG_SIZE, 3)),

        layers.Conv2D(32, (3, 3), activation="relu", padding="same"),
        layers.MaxPooling2D(),

        layers.Conv2D(64, (3, 3), activation="relu", padding="same"),
        layers.MaxPooling2D(),

        layers.Conv2D(128, (3, 3), activation="relu", padding="same"),
        layers.MaxPooling2D(),

        layers.Flatten(),
        layers.Dense(128, activation="relu"),
        layers.Dense(2, activation="softmax")
    ])

    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model

model = build_cnn()
model.summary()

# ============================
# TRAINING
# ============================
history = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=EPOCHS
)

# ============================
# SAVE MODEL (FULL, BUKAN WEIGHTS)
# ============================
output_path = "model_cnn_final_augmented.h5"
model.save(output_path)
print(f"🔥 Model tersimpan full sebagai: {output_path}")
