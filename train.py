import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models
import os

dataset_path = 'set'  # klasör ismini buraya yaz

# Veri arttırma ve yeniden ölçekleme
gen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

# Eğitim ve doğrulama setleri
train_data = gen.flow_from_directory(
    dataset_path,
    target_size=(224, 224),
    batch_size=16,
    class_mode='categorical',
    subset='training'
)

val_data = gen.flow_from_directory(
    dataset_path,
    target_size=(224, 224),
    batch_size=16,
    class_mode='categorical',
    subset='validation'
)

# MobileNetV2 tabanlı model
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation='relu'),
    layers.Dense(5, activation='softmax')  # 5 sınıf
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Eğitimi başlat
model.fit(train_data, validation_data=val_data, epochs=15)

# Modeli kaydet
model.save("yemek_modeli.h5")
