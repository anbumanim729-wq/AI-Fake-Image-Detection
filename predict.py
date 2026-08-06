import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

# Load trained model
model = tf.keras.models.load_model("model.h5")

class_names = ["FAKE", "REAL"]

def predict_image(img_path):

    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)

    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = float(model.predict(img_array, verbose=0)[0][0])

    print("\n==============================")
    print("Raw Prediction :", prediction)
    print("==============================")

    if prediction >= 0.5:
        label = "FAKE"
        confidence = prediction * 100
    else:
        label = "REAL"
        confidence = (1 - prediction) * 100

    print(f"RESULT : {label}")
    print(f"CONFIDENCE : {confidence:.2f}%")
    print("==============================\n")

    return label, round(confidence, 2)