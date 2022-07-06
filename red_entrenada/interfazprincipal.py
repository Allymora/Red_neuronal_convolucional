# Librerias a utilizar
import os
import io
import PySimpleGUI as sg
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import tensorflow as tf
from PIL import Image, UnidentifiedImageError

# extensiones y otros valores usados
file_types = [("JPEG (*.jpg)", "*.jpg"),
              ("All files (*.*)", "*.*")]
longitud, altura = 100, 100
modelo_usar = tf.keras.models.load_model(r'C:\Users\Admin\Downloads\red1\modeloentrenado.h5') #pone donde tenes el modelo


# layouts de columnas
parte_izquierda = [
    [sg.Text("Seleccione imagen")],
    [

        sg.Input(size=(25, 1), key="-FILE-"),
        sg.FileBrowse(file_types=file_types),
        sg.Button("Load Image"),
    ]

]
parte_derecha = [
    [sg.Text("Imagen a Clasificar")],
    [sg.Image(key="-IMAGE-")],
    [sg.Button("Clasificar")]
]

parte_baja = [
    [sg.Text("Resultados")],
    [sg.Multiline(key="contenedor")]
    

]


# fin layouts de columnas

# funcion para predecir imagenes con el modelo
def predict(file):

    x = load_img(file, target_size=(longitud, altura))
    x = img_to_array(x)
    x = np.expand_dims(x, axis=0)
    array = modelo_usar.predict(x)
    result = array[0]
    answer = np.argmax(result)
    if answer == 0:
       print("pred: carton")
    elif answer == 1:
        print("pred: plastico")
    return answer
#fin funcion para predecir

#imprimir resultado
def imprimir_resul(answer):
    if answer==1:
        respuesta="plastico"
    else:
        respuesta="carton"
    window["contenedor"].update(respuesta)

    return respuesta

# All the stuff inside your window. This is the PSG magic code compactor...
sg.theme('DarkBlue8')
layout = [
    [sg.Column(parte_izquierda, size=(350, 200)),
     sg.VSeperator(),
     sg.Column(parte_derecha, size=(800, 400))],
    [sg.Column(parte_baja)]
]

# Create the Window
window = sg.Window('Clasificador de Objetos', layout, size=(800, 600))
# Event Loop to process "events"
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break
    if event == "Load Image":
        filename = values["-FILE-"]
        if os.path.exists(filename):
            image = Image.open(values["-FILE-"])
            image.thumbnail((200, 200))
            bio = io.BytesIO()
            image.save(bio, format="PNG")
            window["-IMAGE-"].update(data=bio.getvalue())
    if event == "Clasificar":
        filename = values["-FILE-"]
        if os.path.exists(filename):
            imprimir_resul(predict(filename))
            

window.close()
