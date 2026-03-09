import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# ============================
# 1. Dataset Grayscale Loader
# ============================

data_dir = "dataset"   # folder dataset (merah / putih)

img_size = (64, 64)
batch_size = 16

datagen = ImageDataGenerator(
    validation_split=0.2,
    rescale=1./255,
    zoom_range=0.15,
    brightness_range=[0.7, 1.3],
)

train_gen = datagen.flow_from_directory(
    data_dir,
    target_size=img_size,
    batch_size=batch_size,
    class_mode="categorical",
    color_mode="grayscale",
    subset="training"
)

val_gen = datagen.flow_from_directory(
    data_dir,
    target_size=img_size,
    batch_size=batch_size,
    class_mode="categorical",
    color_mode="grayscale",
    subset="validation"
)

print("\nLabel classes:", train_gen.class_indices)

# ============================
# 2. Build CNN Grayscale
# ============================

model = models.Sequential([
    layers.Input(shape=(64, 64, 1)),

    layers.Conv2D(32, (3,3), activation='relu'),
    layers.MaxPooling2D(),

    layers.Conv2D(64, (3,3), activation='relu'),
    layers.MaxPooling2D(),

    layers.Conv2D(128, (3,3), activation='relu'),
    layers.MaxPooling2D(),

    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(2, activation='softmax')   # 2 kelas: merah / tidak_merah
])

model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# ============================
# 3. Training
# ============================

history = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=12
)

# ============================
# 4. Save Model
# ============================

model.save("model_cnn_gray.h5")
print("\nModel CNN Grayscale selesai disimpan sebagai model_cnn_gray.h5")
