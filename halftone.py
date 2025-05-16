#Importación de las librerías a utilizar
from PIL import Image
import numpy as np

# Función para obtener las coordenadas de los puntos a dibujar (Predefinida)
def get_grid_coords(h, w, dot_size, angle_deg):
    positions = []
    angle_rad = np.radians(angle_deg)
    cx, cy = w / 2, h / 2  # centro de la imagen

    diag = int(np.sqrt(w ** 2 + h ** 2))
    num_x = diag // dot_size + 3
    num_y = diag // dot_size + 3

    offset_x = cx - (num_x * dot_size) / 2
    offset_y = cy - (num_y * dot_size) / 2

    for i in range(num_y):
        for j in range(num_x):
            gx = offset_x + j * dot_size + dot_size / 2 - cx
            gy = offset_y + i * dot_size + dot_size / 2 - cy
            rx = gx * np.cos(angle_rad) - gy * np.sin(angle_rad) + cx
            ry = gx * np.sin(angle_rad) + gy * np.cos(angle_rad) + cy

            ix, iy = int(round(rx)), int(round(ry))
            if 0 <= iy < h and 0 <= ix < w:
                positions.append((ix, iy))
    return positions

# Filtro halftone principal
def filtro_halftone(ruta:str, dot_size:int=10, angle_deg:list=None)-> Image:
     """ Aplica un filtro Halftone a una imagen en escala de colores RGB. Este filtro simula el patrón de puntos usado en impresión, con diferentes ángulos para cada canal de color
    (rojo, verde y azul). Cuanto más oscura la región, mayor es el tamaño del punto.
    Parámetros:
        ruta (str): Ruta al archivo de imagen.
        dot_size (int): Tamaño base de los puntos. Debe ser positivo. Por defecto es 10.
        angle_deg (list): Lista de tres ángulos de rotación (uno por canal R, G, B). Si no se proporciona, se usan valores por defecto.
        Retorna:
        Image: Imagen procesada con el filtro halftone aplicada."""
     if angle_deg is None: #Debido a un error en la ejecución, conviene realizar la transformación de los ángulos antes de ingresarlos y trabajar con valor None como default.
            angle_deg = [15.75, 45.0, 75.0] #Asignación de los ángulos por Default 
     ruta_imagen= Image.open(ruta) #Abre la imagen 
     imagen = ruta_imagen.convert("RGB") #La convierte en formato "RGB"
     img_array = np.array(imagen) #La almacena como dato array 
     altura, ancho = img_array.shape[:2] #Obtiene las dimensiones de la imagen 

     lienzo = np.ones((altura, ancho, 3), dtype=np.uint8) * 255  # Crea un lienzo blanco para cada canal de color 

        # Separa  canales: rojo, verde y azul 
     canales = [img_array[:, :, i] for i in range(3)]

     for i, canal in enumerate(canales):  # Para R, G, B
            coords = get_grid_coords(altura, ancho, dot_size, angle_deg[i]) #Devuelve una lista de puntos en los que deberán estar centrados los circulos.

            for x, y in coords: #Coordenadas del centro radial 
                intensidad = canal[y, x]  # Retorna la intensidad(0 a 255) de cada pixel en el canal
                radio = int((1 - (intensidad / 255)) * dot_size * 0.7)  # Aplicación de la fórmula del radio

                # Se recorre una ventana cuadrada de tamaño (2 * radio + 1) x (2 * radio + 1) centrada en (x, y)
                for dy in range(-radio, radio + 1): #(y - cy) = dy (diferencial)
                    for dx in range(-radio, radio + 1):# (x - cx) = dx (diferencial)
                        nx = x + dx 
                        ny = y + dy
                        if 0 <= nx < ancho and 0 <= ny < altura:
                            if dx ** 2 + dy ** 2 <= radio ** 2: #Esto asegura que se pinten solo los píxeles dentro o sobre el borde del círculo.
                                lienzo[ny, nx, i] = 0  # Se pinta el lienzo para cada canal de color
        # Convertir la nueva imagen a formato Pillow y guardar
     nueva_imagen_array = np.array(lienzo, dtype=np.uint8)
     imagen_resultado= Image.fromarray(nueva_imagen_array)
     return(imagen_resultado)
    # stack = np.hstack((img_array, lienzo))
    # return Image.fromarray(stack)
# #PruebadelFiltro
# prueba=filtro_halftone(ruta, 8,[15,45, 30])
# prueba.show()

 