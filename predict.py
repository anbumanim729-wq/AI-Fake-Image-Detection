import os

# TensorFlow CPU thread usage limit
os.environ["TF_NUM_INTRAOP_THREADS"] = "1"
os.environ["TF_NUM_INTEROP_THREADS"] = "1"

import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image


# =========================================================
# LOAD MODEL
# =========================================================

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "model.h5"
)

print("Loading TruthLens model...")
print("Model path:", MODEL_PATH)

model = tf.keras.models.load_model(
    MODEL_PATH,
    compile=False
)

print("TruthLens model loaded successfully.")

class_names = ["FAKE", "REAL"]


# =========================================================
# PREDICTION
# =========================================================

def predict_image(img_path):

    print("===================================")
    print("Prediction started")
    print("Image:", img_path)
    print("===================================")

    # -----------------------------------------------------
    # LOAD IMAGE
    # -----------------------------------------------------

    img = image.load_img(
        img_path,
        target_size=(224, 224)
    )

    img_array = image.img_to_array(img)

    # -----------------------------------------------------
    # NORMALIZE
    # -----------------------------------------------------

    img_array = img_array.astype("float32") / 255.0

    # -----------------------------------------------------
    # ADD BATCH DIMENSION
    # -----------------------------------------------------

    img_array = np.expand_dims(
        img_array,
        axis=0
    )

    print("Image prepared:", img_array.shape)

    # -----------------------------------------------------
    # PREDICT
    # -----------------------------------------------------

    prediction = model.predict(
        img_array,
        verbose=0
    )

    prediction = float(
        prediction[0][0]
    )

    print("Raw Prediction:", prediction)

    # -----------------------------------------------------
    # RESULT
    # -----------------------------------------------------

    if prediction >= 0.5:

        label = "FAKE"

        confidence = prediction * 100

    else:

        label = "REAL"

        confidence = (1 - prediction) * 100

    confidence = round(
        confidence,
        2
    )

    print("RESULT:", label)
    print("CONFIDENCE:", confidence)
    print("===================================")

    return label, confidence