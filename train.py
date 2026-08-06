import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import (
    EarlyStopping,
    ReduceLROnPlateau,
    ModelCheckpoint
)

# ==========================
# SETTINGS
# ==========================

IMG_SIZE = 160
BATCH_SIZE = 64
EPOCHS = 5

# ==========================
# DATASET PATH
# ==========================

train_path = r"C:\Users\acer\OneDrive\Desktop\AI-Fake-Image-Detection\dataset\archive\train"

test_path = r"C:\Users\acer\OneDrive\Desktop\AI-Fake-Image-Detection\dataset\archive\test"

# ==========================
# DATA AUGMENTATION
# ==========================

train_datagen = ImageDataGenerator(

    preprocessing_function=preprocess_input,

    rotation_range=20,

    width_shift_range=0.2,

    height_shift_range=0.2,

    zoom_range=0.2,

    shear_range=0.2,

    horizontal_flip=True,

    brightness_range=[0.8, 1.2],

    fill_mode="nearest"

)

test_datagen = ImageDataGenerator(

    preprocessing_function=preprocess_input

)

# ==========================
# TRAIN DATA
# ==========================

train_data = train_datagen.flow_from_directory(

    train_path,

    target_size=(IMG_SIZE, IMG_SIZE),

    batch_size=BATCH_SIZE,

    class_mode="binary",

    shuffle=True

)

# ==========================
# TEST DATA
# ==========================

test_data = test_datagen.flow_from_directory(

    test_path,

    target_size=(IMG_SIZE, IMG_SIZE),

    batch_size=BATCH_SIZE,

    class_mode="binary",

    shuffle=False

)

print("\n==============================")
print("Class Labels")
print("==============================")
print(train_data.class_indices)

# ==========================
# LOAD MOBILENETV2
# ==========================

base_model = MobileNetV2(

    weights="imagenet",

    include_top=False,

    input_shape=(IMG_SIZE, IMG_SIZE, 3)

)

base_model.trainable = False
# ==========================
# BUILD MODEL
# ==========================

model = Sequential([

    base_model,

    GlobalAveragePooling2D(),

    Dense(
        256,
        activation="relu"
    ),

    Dropout(0.4),

    Dense(
        128,
        activation="relu"
    ),

    Dropout(0.3),

    Dense(
        1,
        activation="sigmoid"
    )

])

# ==========================
# COMPILE MODEL
# ==========================

model.compile(

    optimizer=Adam(
        learning_rate=1e-4
    ),

    loss="binary_crossentropy",

    metrics=["accuracy"]

)

print("\n===================================")
print(" MobileNetV2 Model ")
print("===================================\n")

model.summary()

# ==========================
# CALLBACKS
# ==========================

checkpoint = ModelCheckpoint(

    "best_model.keras",

    monitor="val_accuracy",

    save_best_only=True,

    verbose=1

)

early_stop = EarlyStopping(

    monitor="val_loss",

    patience=2,

    restore_best_weights=True,

    verbose=1

)

reduce_lr = ReduceLROnPlateau(

    monitor="val_loss",

    factor=0.5,

    patience=1,

    min_lr=1e-7,

    verbose=1

)

# ==========================
# FIRST TRAINING
# ==========================

print("\n===================================")
print(" Training Started ")
print("===================================\n")

history = model.fit(

    train_data,

    validation_data=test_data,

    epochs=EPOCHS,

    callbacks=[

        checkpoint,

        early_stop,

        reduce_lr

    ],

    verbose=1

)

print("\nLoading Best Model...\n")

model = tf.keras.models.load_model(

    "best_model.keras"

)
# ==========================
# LOAD BEST MODEL
# ==========================

print("\nLoading Best Model...\n")

model = tf.keras.models.load_model("best_model.keras")

# ==========================
# TEST MODEL
# ==========================

loss, accuracy = model.evaluate(test_data, verbose=1)

print(f"\nTest Loss     : {loss:.4f}")
print(f"Test Accuracy : {accuracy*100:.2f}%")

# ==========================
# SAVE MODEL
# ==========================

model.save("model.h5")

print("\n===================================")
print(" MODEL TRAINING COMPLETED ")
print("===================================")

print("✔ Best Model  : best_model.keras")
print("✔ Final Model : model.h5")
print(f"✔ Final Accuracy : {accuracy*100:.2f}%")