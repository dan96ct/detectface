# -*- coding: latin-1 -*-
"""
    Código 2.1 - Reconocimiento facial en una imagen estática
    Este programa identifica varios rostros de físicos famosos en fotografías.
 
    Escrito por Glare y Transductor
    www.robologs.net

    NOTA: Codigo adaptado para sacar los rostros de la carpeta database y cotejarlos con la carpeta search
    en caso de no encontrar el rostro elimina la imagen
"""
import cv2
import face_recognition

import os
from os import listdir
from os.path import isfile, join

pathDatabase = 'database/'
pathSearch = 'search/'

database = [f for f in listdir(pathDatabase) if isfile(join(pathDatabase, f))]
search = [f for f in listdir(pathSearch) if isfile(join(pathSearch, f))]

encodings_conocidos = []
nombres_conocidos = []

for data in database:
     imagen_data = face_recognition.load_image_file(pathDatabase + data)
     data_encoding = face_recognition.face_encodings(imagen_data)[0]
     encodings_conocidos.append(data_encoding)
     nombres_conocidos.append(data)
 
#Cargamos una fuente de texto:
font = cv2.FONT_HERSHEY_COMPLEX
 
 
for imgName in search:
     img = pathSearch + imgName
     img = face_recognition.load_image_file(img)
     # Definir tres arrays, que servirán para guardar los parámetros de los rostros que se encuentren en la imagen:
     loc_rostros = [] #Localizacion de los rostros en la imagen (contendrá las coordenadas de los recuadros que las contienen)
     encodings_rostros = [] #Encodings de los rostros
     nombres_rostros = [] #Nombre de la persona de cada rostro
     
     
     #Localizamos cada rostro de la imagen y extraemos sus encodings:
     loc_rostros = face_recognition.face_locations(img)
     encodings_rostros = face_recognition.face_encodings(img, loc_rostros)
     
     
     #Recorremos el array de encodings que hemos encontrado:
     eliminar = True
     for encoding in encodings_rostros:
     
          #Buscamos si hay alguna coincidencia con algún encoding conocido:
          coincidencias = face_recognition.compare_faces(encodings_conocidos, encoding)
          
          #El array 'coincidencias' es ahora un array de booleanos.
          #Si contiene algun 'True', es que ha habido alguna coincidencia:
          if True in coincidencias:
               #Buscamos el nombre correspondiente en el array de nombres conocidos:
               nombre = nombres_conocidos[coincidencias.index(True)]
               print('Coincidencia encontrada ------>'  + nombre)
               eliminar = False
          
          #Si no hay ningún 'True' en el array 'coincidencias', no se ha podido identificar el rostro:
          else:
               nombre = "???"
          
          #Añadimos el nombre de la persona identificada en el array de nombres:
          nombres_rostros.append(nombre)
          
          
     #Dibujamos un recuadro rojo alrededor de los rostros desconocidos, y uno verde alrededor de los conocidos:
     for (top, right, bottom, left), nombre in zip(loc_rostros, nombres_rostros):
               
          #Cambiar el color segun el nombre:
          if nombre != "???":
               color = (0,255,0) #Verde
          else:
               color = (0,0,255) #Rojo
               
          #Dibujar los recuadros alrededor del rostro:
          cv2.rectangle(img, (left, top), (right, bottom), color, 2)
          cv2.rectangle(img, (left, bottom - 20), (right, bottom), color, -1)
               
          #Escribir el nombre de la persona:
          cv2.putText(img, nombre, (left, bottom - 6), font, 0.6, (0,0,0), 1)
     
     #Abrimos una ventana con el resultado:
     cv2.imshow('Output', img)
     #cv2.waitKey(200)
     cv2.destroyAllWindows()
     if eliminar:
          os.remove(pathSearch + imgName)
     