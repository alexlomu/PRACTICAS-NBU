import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Definir modelo CNN
model = Sequential([
    Conv2D(32, (3,3), activation="relu", input_shape=(128,128,3)),
    MaxPooling2D((2,2)),
    Flatten(),
    Dense(128, activation="relu"),
    Dense(10, activation="softmax")  # 10 niveles de calificación
])

model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

# Cargar imágenes de entrenamiento
datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)
train_generator = datagen.flow_from_directory("../data/train", target_size=(128,128), batch_size=32, class_mode="sparse", subset="training")
val_generator = datagen.flow_from_directory("../data/train", target_size=(128,128), batch_size=32, class_mode="sparse", subset="validation")

# Entrenar el modelo
model.fit(train_generator, validation_data=val_generator, epochs=10)

# Guardar modelo
model.save("../models/grading_model.h5")
