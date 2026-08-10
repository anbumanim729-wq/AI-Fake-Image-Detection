# =========================================================
# TRUTHLENS - IMAGE PREDICTION
# predict.py
# =========================================================

import os

# =========================================================
# MEMORY / CPU SETTINGS
# IMPORTANT: These must be set BEFORE TensorFlow import
# =========================================================

os.environ["TF_NUM_INTRAOP_THREADS"] = "1"
os.environ["TF_NUM_INTEROP_THREADS"] = "1"

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

# Reduce unnecessary TensorFlow logs
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"


# =========================================================
# IMPORTS
# =========================================================

import tensorflow as tf
import numpy as np

from tensorflow.keras.utils import load_img
from tensorflow.keras.utils import img_to_array


# =========================================================
# TENSORFLOW THREAD CONFIGURATION
# =========================================================

try:

    tf.config.threading.set_intra_op_parallelism_threads(1)

    tf.config.threading.set_inter_op_parallelism_threads(1)

except Exception as e:

    print(
        "TensorFlow thread configuration:",
        e
    )


# =========================================================
# MODEL PATH
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "model.h5"
)


# =========================================================
# START MODEL
# =========================================================

print("==========================================")
print("          TRUTHLENS AI MODEL")
print("==========================================")

print(
    "Loading TruthLens model..."
)

print(
    "Model path:",
    MODEL_PATH
)


# =========================================================
# CHECK MODEL
# =========================================================

if not os.path.exists(MODEL_PATH):

    raise FileNotFoundError(
        "model.h5 not found: "
        + MODEL_PATH
    )


# =========================================================
# LOAD MODEL
# =========================================================

try:

    model = tf.keras.models.load_model(
        MODEL_PATH,
        compile=False
    )

except Exception as e:

    print(
        "MODEL LOAD ERROR:",
        e
    )

    raise


print(
    "TruthLens model loaded successfully."
)


# =========================================================
# MODEL INFORMATION
# =========================================================

print(
    "Model input shape:",
    model.input_shape
)

print(
    "Model output shape:",
    model.output_shape
)

print("==========================================")


# =========================================================
# CLASS NAMES
# =========================================================

class_names = [
    "FAKE",
    "REAL"
]


# =========================================================
# GET MODEL IMAGE SIZE
# =========================================================

def get_image_size():

    input_shape = model.input_shape

    # Expected:
    # (None, height, width, channels)

    if (
        len(input_shape) != 4
        or input_shape[1] is None
        or input_shape[2] is None
    ):

        # Fallback
        return 224, 224


    height = int(
        input_shape[1]
    )

    width = int(
        input_shape[2]
    )

    return height, width


# =========================================================
# PREDICT IMAGE
# =========================================================

def predict_image(img_path):

    print("==========================================")
    print("Prediction started")
    print("Image:", img_path)
    print("==========================================")


    # =====================================================
    # CHECK IMAGE PATH
    # =====================================================

    if not img_path:

        raise ValueError(
            "Image path is empty."
        )


    if not os.path.exists(img_path):

        raise FileNotFoundError(
            "Image not found: "
            + img_path
        )


    # =====================================================
    # GET MODEL IMAGE SIZE
    # =====================================================

    image_height, image_width = (
        get_image_size()
    )


    print(
        "Target image size:",
        image_height,
        "x",
        image_width
    )


    # =====================================================
    # LOAD IMAGE
    # =====================================================

    img = load_img(
        img_path,
        target_size=(
            image_height,
            image_width
        ),
        color_mode="rgb"
    )


    print(
        "Image loaded successfully."
    )


    # =====================================================
    # IMAGE → NUMPY ARRAY
    # =====================================================

    img_array = img_to_array(
        img
    )


    print(
        "Original array shape:",
        img_array.shape
    )


    # =====================================================
    # NORMALIZATION
    # =====================================================

    img_array = (
        img_array
        .astype("float32")
        / 255.0
    )


    # =====================================================
    # ADD BATCH DIMENSION
    # =====================================================

    img_array = np.expand_dims(
        img_array,
        axis=0
    )


    print(
        "Final input shape:",
        img_array.shape
    )


    # =====================================================
    # AI PREDICTION
    #
    # Direct model call is lighter than model.predict()
    # for a single image.
    # =====================================================

    print(
        "Running AI prediction..."
    )


    input_tensor = tf.convert_to_tensor(
        img_array,
        dtype=tf.float32
    )


    prediction = model(
        input_tensor,
        training=False
    )


    # Convert TensorFlow tensor to NumPy
    prediction = prediction.numpy()


    print(
        "Raw prediction:",
        prediction
    )

    print(
        "Prediction shape:",
        prediction.shape
    )


    # =====================================================
    # SINGLE OUTPUT MODEL
    #
    # Example:
    # [[0.73]]
    # =====================================================

    if (
        prediction.ndim == 2
        and prediction.shape[1] == 1
    ):

        score = float(
            prediction[0][0]
        )


        # -----------------------------------------------
        # Clamp score
        # -----------------------------------------------

        score = max(
            0.0,
            min(
                1.0,
                score
            )
        )


        # -----------------------------------------------
        # Classification
        # -----------------------------------------------

        if score >= 0.5:

            label = "FAKE"

            confidence = (
                score * 100
            )

        else:

            label = "REAL"

            confidence = (
                (1.0 - score) * 100
            )


    # =====================================================
    # TWO OUTPUT MODEL
    #
    # Example:
    # [[0.20, 0.80]]
    # =====================================================

    elif (
        prediction.ndim == 2
        and prediction.shape[1] == 2
    ):

        probabilities = (
            prediction[0]
        )


        # -----------------------------------------------
        # Get highest probability
        # -----------------------------------------------

        predicted_class = int(
            np.argmax(
                probabilities
            )
        )


        # -----------------------------------------------
        # Safety check
        # -----------------------------------------------

        if predicted_class >= len(
            class_names
        ):

            raise ValueError(
                "Invalid predicted class: "
                + str(predicted_class)
            )


        label = class_names[
            predicted_class
        ]


        confidence = (
            float(
                probabilities[
                    predicted_class
                ]
            ) * 100
        )


    # =====================================================
    # UNKNOWN OUTPUT
    # =====================================================

    else:

        raise ValueError(
            "Unsupported model output shape: "
            + str(prediction.shape)
        )


    # =====================================================
    # CONFIDENCE LIMIT
    # =====================================================

    confidence = max(
        0.0,
        min(
            100.0,
            confidence
        )
    )


    confidence = round(
        confidence,
        2
    )


    # =====================================================
    # RESULT
    # =====================================================

    print("==========================================")
    print("          TRUTHLENS RESULT")
    print("==========================================")

    print(
        "Result:",
        label
    )

    print(
        "Confidence:",
        confidence,
        "%"
    )

    print("==========================================")


    # =====================================================
    # RETURN
    # =====================================================

    return label, confidence

