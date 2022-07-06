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
#datos sobre el plastico
datos_plastico="""Cada minuto, se vende un millón de botellas de plástico en todo el mundo.
Cada botella de plástico tarda unos 450 años en descomponerse. Si no está a la intemperie, la cifra se aproxima a los 1.000 años.
Más del 90% de los plásticos del mundo se producen a partir de combustibles fósiles.
El 42% del plástico utilizado en el mundo se destina al empaquetado de alimentos y productos manufacturados. Es decir, plásticos de un solo uso que apenas pasan unos minutos en las manos e los consumidores."""

datos_carton="""Por cada tonelada de cartón que se recicla se ahorran 140 litros de petróleo, cincuenta mil litros de agua y 900 kilos de dióxido de carbono (CO2)
ocupa un papel importante en el embalaje de envíos, por encima de los plásticos, la madera y el metal
El contenedor azul no es un cajón de sastre. Para lograr recuperar la mayor cantidad de cartón que pueda ser reciclado en su destino, es necesario que el consumidor conozca las normas de actuación de los contenedores azules, los dedicados a este tipo de residuos.

Los productos que se pueden dejar en este depósito son: periódicos, revistas, cajas o embalajes de cartón y bolsas de papel.
Por otro lado, lo que no debemos echar en ellos es el papel de cocina, las servilletas de papel que están manchadas, los tetra bricks, el papel de aluminio o sanitario, cartones manchados con grasa, así como las etiquetas adhesivas, las fotos y las radiografías"""

# layouts de columnas
parte_izquierda = [
    [sg.Text("Seleccione imagen", background_color="#25D051")],
    [

        sg.Input(size=(25, 1), key="-FILE-"),
        sg.FileBrowse(file_types=file_types),
        sg.Button("Load Image"),
    ]

]
parte_derecha = [
    [sg.Text("Imagen a Clasificar", background_color="#25D051")],
    [sg.Text(size=(40, 1), key="-TEXT-")],
    [sg.Image(key="-IMAGE-")],
    [sg.Button("Clasificar")]
]

parte_baja = [
    [sg.Text("Resultados", background_color="#25D051")],
    [sg.Multiline(size=(30, 5), key='textbox')],
    [sg.Image(key="contenedor")]

]
parte_baja2 = [
    [sg.Text("Relacionado", background_color="#25D051")],
    [sg.Multiline(size=(30, 5), key='textbox2')],
    [sg.Image(key="contenedor")]

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
       pred="carton"
       window["textbox2"].update(datos_carton)
    elif answer == 1:
        pred="plastico"
        window["textbox2"].update(datos_plastico)
    return pred


#fin funcion para predecir

#funciones extras
def reciclaje():

    return
#fin funciones extras

# All the stuff inside your window. This is the PSG magic code compactor...
sg.theme('darkAmber')
layout = [
    [sg.Column(parte_izquierda, size=(350, 200), background_color="#107384"),
     sg.VSeperator(),
     sg.Column(parte_derecha, size=(400, 400), background_color="#275D70")],
    [sg.Column(parte_baja, background_color="#008992"),
    sg.VSeperator(),
    sg.Column(parte_baja2, size=(200, 200), background_color="#008992")]
]

# Create the Window
window = sg.Window('GREENWISH', layout, size=(800, 600), background_color="#00B69C")
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
            window["textbox"].update(predict(filename))
            

window.close()
