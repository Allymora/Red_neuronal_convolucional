# -*- coding: utf-8 -*-
"""Reciclaje_v2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13hPw66Mb9kdjTwQ2IZhsey4T-QfHhG3i
"""

#trabajamos con una version anterior de tensorflow
!pip uninstall tensorflow
!pip install tensorflow==2.7.0

# Commented out IPython magic to ensure Python compatibility.
#crear el directorio del set de datos
# %mkdir ./input
# %mkdir -p ./input/test/test
# %mkdir -p ./input/train/train
# %mkdir -p ./input/train/train/plastico
# %mkdir -p ./input/train/train/carton
# %mkdir -p ./input/test/test/plastico
# %mkdir -p ./input/test/test/carton

import os

print(os.listdir("./input"))
from fastai.vision import *

#librerias a utilizar
import sys
import os
import tensorflow as tf

from tensorflow.python.keras import optimizers
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dropout, Flatten, Dense, Activation
from tensorflow.python.keras.layers import  Convolution2D, MaxPooling2D
from tensorflow.python.keras import backend as K
from tensorflow.keras.preprocessing.image import ImageDataGenerator

K.clear_session()



data_entrenamiento = './input/train/train'
data_validacion = './input/test/test'

#parametros
epocas=3 #normalmente serian 10, pero cada epoca dura bastante
longitud, altura = 100, 100
batch_size = 32
pasos = 1000
validation_steps = 300
filtrosConv1 = 32
filtrosConv2 = 64
tamano_filtro1 = (3, 3)
tamano_filtro2 = (2, 2)
tamano_pool = (2, 2)
clases = 2
lr = 0.0004


##Preparamos nuestras imagenes

entrenamiento_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.3,
    zoom_range=0.3,
    horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1. / 255)

entrenamiento_generador = entrenamiento_datagen.flow_from_directory(
    data_entrenamiento,
    target_size=(altura, longitud),
    batch_size=batch_size,
    class_mode='categorical')

validacion_generador = test_datagen.flow_from_directory(
    data_validacion,
    target_size=(altura, longitud),
    batch_size=batch_size,
    class_mode='categorical')

#arquitectura
cnn = Sequential()
cnn.add(Convolution2D(filtrosConv1, tamano_filtro1, padding ="same", input_shape=(longitud, altura,3), activation='relu'))
cnn.add(MaxPooling2D(pool_size=tamano_pool))

cnn.add(Convolution2D(filtrosConv2, tamano_filtro2, padding ="same"))
cnn.add(MaxPooling2D(pool_size=tamano_pool))

cnn.add(Flatten())
cnn.add(Dense(256, activation='relu'))
cnn.add(Dropout(0.5))
cnn.add(Dense(clases, activation='softmax'))

cnn.compile(loss='categorical_crossentropy',
            optimizer="adam",
            metrics=['accuracy'])



#Entrenamos :)
cnn.fit_generator(
    entrenamiento_generador,
    steps_per_epoch=pasos,
    epochs=epocas,
    validation_data=validacion_generador,
    validation_steps=validation_steps)

#Realizar predicciones
from keras.preprocessing.image import load_img, img_to_array
import numpy as np
def predict(file):
  x = load_img(file, target_size=(longitud, altura))
  x = img_to_array(x)
  x = np.expand_dims(x, axis=0)
  array = cnn.predict(x)
  result = array[0]
  answer = np.argmax(result)
  if answer == 0:
    print("pred: carton")
  elif answer == 1:
    print("pred: plastico")
 

  return answer

#gurdar modelo
cnn.save('modeloentrenado.h5')

#montamos drive
from google.colab import drive
drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
#exportar modelo a drive
# %cp ./modeloentrenado.h5 ./drive/MyDrive

#prueba1

predict('./input/test/test/plastico/p170.jpg')

predict('./input/test/test/plastico/p170.jpg')