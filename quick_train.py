import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping


train_path = "dataset/archive/train"
test_path = "dataset/archive/test"


IMG_SIZE = (224,224)
BATCH_SIZE = 32


train_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,
    horizontal_flip=True
)


train_data = train_datagen.flow_from_directory(
    train_path,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="binary",
    subset="training"
)
print("Class Indices:", train_data.class_indices)

val_data = train_datagen.flow_from_directory(
    train_path,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="binary",
    subset="validation"
)
print("Training Samples:", train_data.samples)
print("Validation Samples:", val_data.samples)


base_model = MobileNetV2(
    weights="imagenet",
    include_top=False,
    input_shape=(224,224,3)
)


base_model.trainable = False


x = base_model.output
x = GlobalAveragePooling2D()(x)

output = Dense(
    1,
    activation="sigmoid"
)(x)


model = Model(
    inputs=base_model.input,
    outputs=output
)


model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)


early_stop = EarlyStopping(
    patience=2,
    restore_best_weights=True
)


model.fit(
    train_data,
    validation_data=val_data,
    epochs=5,
    callbacks=[early_stop]
)


model.save("model.h5")


print("MODEL SAVED SUCCESSFULLY")