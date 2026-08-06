import tensorflow as tf

model = tf.keras.models.load_model("best_model.keras")
model.save("model.h5")

print("Done! model.h5 created successfully.")