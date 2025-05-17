#Importación de las librerías a utilizar 
import numpy as np
from PIL import Image
import random
#Proceso de edición de imagen por método K-Means
def filtro_Kmeans(ruta: str, colores: int = 8) -> Image:
     """ Aplica una cuantización  usando el algoritmo K-Means a una imagen.Este filtro reduce
        la cantidad de colores en la imagen original a un número específico  de colores,
        generando una versión simplificada basada en agrupaciones de colores denominadas clusters. 
        Parámetros:
        ruta (str): Ruta al archivo de imagen.
        colores (int): Número de colores (clusters) a utilizar en la cuantización. Por defecto es 8.
        Retorna:
        Image: Imagen en formato Pillow."""
    
    

     imagen_pillow = Image.open(ruta).convert("RGB") # Abre la imagen y la convierte a formato RGB
     imagen = np.array(imagen_pillow) # Convierte la imagen en un array NumPy
     alto, ancho, _ = imagen.shape #Obtiene las dimensiones de la imagen 

    # Reorganiza la imagen en una matriz de pixeles (N, 3)
     pixeles = imagen.reshape(-1, 3)

    # Inicializa  k centroides aleatoriamente desde los píxeles
     indices = np.random.choice(len(pixeles), size=colores, replace=False)
     centroides = pixeles[indices].astype(float)  

     for _ in range(100): #Máximo de 100 iteraciones para la formación de los clusters 
        # Calcula la  distancia de cada píxel a cada centroide → (N, K)
        distancias = np.linalg.norm(pixeles[:, None] - centroides[None, :], axis=2)

        # Asigna cada píxel al centroide más cercano → (N,)
        asignaciones = np.argmin(distancias, axis=1)

        # Calcula nuevos centroides
        nuevos_centroides = []#Inicializa una lista para almacenar los nuevos centroides
        for i in range(colores):
            grupo = pixeles[asignaciones == i]
            if len(grupo) > 0:
                nuevo_centroide = np.mean(grupo, axis=0)
            else:
                nuevo_centroide = pixeles[np.random.randint(0, len(pixeles))]
            nuevos_centroides.append(nuevo_centroide)

        nuevos_centroides = np.array(nuevos_centroides)

        # Verifica si los centroides continúan variando 
        if np.allclose(centroides, nuevos_centroides, atol=1):
            break

        centroides = nuevos_centroides # Actualiza los centroides

    # Reemplaza cada  píxel por su centroide asignado
     pixeles_cuantizados = centroides[asignaciones].astype(np.uint8)
     imagen_cuantizada = pixeles_cuantizados.reshape((alto, ancho, 3))
      # Convierte la nueva imagen a formato Pillow
     return Image.fromarray(imagen_cuantizada)
     


#Prueba
# prueba= filtro_Kmeans("tulips.png", 8)

# prueba.show()
