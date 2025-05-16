from halftone import filtro_halftone
from k_means_opti import filtro_Kmeans
from pathlib import Path
import numpy as np
from PIL import Image
#Datos solicitados al usuario 
# Solicita al usuario la ruta de la imagen
ruta_imagen=input("Ingrese al ruta de la imagen 📷: ") 

# Verifica si la ruta existe y es un archivo válido
# if not Path(ruta_imagen).exists():
#     print("No se encontró la imagen. Por favor, verifique la ruta e intente nuevamente.")

try:
    with open(ruta_imagen, 'rb'):
        pass #Continúa la ejecución del progama si encuentra a la imagen 
except FileNotFoundError:
    print("No se encontró la imagen. Por favor, verifique la ruta e intente nuevamente.")
    exit(1)  # Termina la ejecución del programa 

#Abre la imagen 
imagen= Image.open(ruta_imagen) #Ingreso de la imagen al programa 
#Solicita el ingreso del método
metodo= input("Seleccione el método de cuantización (halftone/kmeans): ")

while(metodo.lower()!="halftone" and metodo.lower()!="kmeans"): #Controla que el método esté bien escrito 
    print("Por favor, escriba correctamente el método que desea aplicar.")
    metodo= input("Seleccione el método de cuantización (halftone/kmeans): ")
if metodo.lower()=="halftone": #Ejecución del proceso halftone 
        tamaño_puntos= int(input("Ingrese el tamaño de los puntos: ")) #Debe ser entero 
        while tamaño_puntos<=0:
            print("El tamaño de los puntos debe ser un número positivo.")
            tamaño_puntos= int(input("Ingrese el tamaño de los puntos: "))
        angulos_solicitados= input("Ingrese los ángulos de rotación para los canales RGB (separados por comas): ") #Solicita el ingreso de los ángulos 
        angulos_rot=  [float(valor.strip()) for valor in angulos_solicitados.split(',')] #Los transforma en float y los organiza en una lista 
        #imagen= Image.open(ruta_imagen)
        halftone_imagen= filtro_halftone(ruta_imagen, tamaño_puntos, angulos_rot) #Aplicación de la función
        halftone_imagen.show() #Muestra la imagen editada
        halftone_imagen.save("halftone_imagen.jpg") #La guarda con el filtro Halftone aplicado

elif metodo.lower()=="kmeans": #Ejeccución del proceso k-Means
     colores= int(input("Ingrese el número de colores deseados: ")) #Solicita los colores o  los k (futuros centroides)
     k_means_imagen = filtro_Kmeans(ruta_imagen, colores) #Inicializa el proceso 
     k_means_imagen.show() #Muestra la imagen editada
     k_means_imagen.save("k_means_imagen.jpg") #Guarda la imagen con el filtro K-means
#Image.close() #Cierra la imagen 