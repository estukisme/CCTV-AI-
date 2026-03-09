import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
import os

# =====================================================================
# PATH DATASET
# =====================================================================
base_dir = r"D:\2026\PHONSKA 1\CCTV\dataset_split"

train_dir = os.path.join(base_dir, "train")
val_dir   = os.path.join(base_dir, "val")
test_dir  = os.path.join(base_dir, "test")

# =====================================================================
# HYPERPARAMETER
# =====================================================================
IMG_SIZE = (64, 64)
BATCH    = 32
EPOCHS   = 25
LR       = 1e-4

# =====================================================================
# AUGMENTASI PRIBADI SESUAI DATASET KAK JUN
# =====================================================================

train_gen = ImageDataGenerator(
    rescale=1/255.,
    
    # Perubahan umum
    rotation_range=10,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.15,
    shear_range=0.1,
    
    # Perubahan warna yg sering terjadi di CCTV
    brightness_range=[0.6, 1.4],
    channel_shift_range=25,  # memperbaiki shifting coklat → merah
    
    # Noise karena RTSP
    horizontal_flip=False,
    vertical_flip=False
)

val_gen = ImageDataGenerator(rescale=1/255.)
test_gen = ImageDataGenerator(rescale=1/255.)

train_data = train_gen.flow_from_directory(
    train_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH,
    class_mode="categorical"
)

val_data = val_gen.flow_from_directory(
    val_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH,
    class_mode="categorical"
)

test_data = test_gen.flow_from_directory(
    test_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH,
    class_mode="categorical"
)

# =====================================================================
# CNN MODEL V2 — LEBIH DALAM DAN STABIL
# =====================================================================

model = Sequential([
    Conv2D(32, (3,3), activation='relu', padding="same", input_shape=(64,64,3)),
    BatchNormalization(),
    MaxPooling2D(2,2),

    Conv2D(64, (3,3), activation='relu', padding="same"),
    BatchNormalization(),
    MaxPooling2D(2,2),

    Conv2D(128, (3,3), activation='relu', padding="same"),
    BatchNormalization(),
    MaxPooling2D(2,2),
    
    Flatten(),
    Dense(256, activation='relu'),
    Dropout(0.4),
    
    Dense(2, activation='softmax')
])

model.compile(
    optimizer=Adam(LR),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# =====================================================================
# TRAINING
# =====================================================================

history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS,
    batch_size=BATCH
)

# =====================================================================
# EVALUASI (penting supaya threshold aman)
# =====================================================================

print("\nEvaluasi Test Set:")
model.evaluate(test_data)

# =====================================================================
# EXPORT MODEL
# =====================================================================
model.save("model_cnn_v2.h5")
print("\nModel tersimpan: model_cnn_v2.h5")