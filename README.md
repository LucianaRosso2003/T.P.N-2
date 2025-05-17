# T.P.N-2: Filtros de imagen  Halftone y K-Means Quantization

Este proyecto permite procesar imágenes mediante la aplicación de dos métodos de cuantización de colores utilizando Python: filtro Halftone y  la cuantización con K-Means. 


## Partes y funciones  del proyecto

- `script.py`: archivo principal a ejecutar  que gestiona la entrada del usuario, carga la imagen y aplica el filtro seleccionado. Luego, muestra la imagen resultante de aplicar el método de cuantización y la guarda como archivo. 
- `halftone.py`: contiene la implementación del filtro Halftone y la función predefinida get_grid_coords. 
- `k_means_opt.py`: contiene la implementación del filtro de cuantización por K-Means.

## Requisitos

Antes de ejecutar el proyecto debe instalarse numpy y PIL

## Instrucciones para implementar el código 
1) Agregar la imagen que desea procesar en el mismo directorio en el que se encuentra el script.
2) Ejecuta el archivo principal: script.py
3) El programa solicitará:
   3.a) Ingreso de  la ruta de la imagen.
   3.b) Elección  del filtro a aplicar: Halftone o K-Means.
   3.c) #En el caso de seleccionar Halftone se pedirá tamaño de los puntos (dot_size) y  el ángulo de rotación para cada 
         canal de color (RGB).
        #En caso de elegir K-Means,  el número de colores (clusters) deseado.
4) Una vez aplicado el filtro seleccionado se muestra la imagen con el filtro aplicado y se guarda como "k_means_imagen.jpg" o "halftone_imagen.jpg"

## LÓGICA DE CADA FILTRO 
### HALFTONE
El filtro Halftone simula el efecto de impresión tradicional por semitonos utilizando círculos de colores primarios (rojo, verde y azul) de distintos tamaños. La idea es reemplazar cada grupo de píxeles por un punto cuyo radio depende de la intensidad del color en ese lugar, creando una imagen compuesta por patrones de puntos.
1) Separación por canales:
   - La imagen se divide en sus tres canales RGB.
   - Cada canal será procesado por separado para generar un patrón de puntos distinto.

2) Creación de matriz base:
- Se genera una nueva matriz  del mismo tamaño que la imagen para cada canal  inicializada  con valores 255 (color blanco en escala de grises).

3) Cálculo de coordenadas de la grilla:
   - Se llama a una función get_grid_coords que devuelve una lista de coordenadas (x, y). Esta función utiliza el tamaño del punto y un ángulo de rotación que es propio de cada canal de color.

4) Cálculo del radio del círculo:
Para cada punto de la grilla, se toma el valor de intensidad del píxel correspondiente en el canal original.
Se calcula el radio r del círculo usando la fórmula:
radio = (1- I/255)* dot_size *0.7
Donde 
I es la intensidad del píxel (de 0 a 255).
dot_size: es el tamaño de los puntos 
Esto significa que cuanto más claro(próximo a blanco) sea el píxel, mayor será el círculo.
5) Dibujo del círculo: 
En la matriz blanca se dibuja un círculo  centrado en la coordenada  con el radio calculado.
Se utilizan las condiciones geométricas para pintar todos los píxeles  dentro del círculo.
6) Formación de la imagen final:
Una vez procesados los tres canales (cada uno con su propio patrón), se combinan nuevamente en una imagen RGB para generar la versión final con efecto halftone.
###K-MEANS
Este filtro aplica cuantización de colores mediante el algoritmo K-Means, lo que reduce la cantidad de colores de una imagen agrupando los píxeles en un número k de clausters.
1) Transformación de la imagen ingresada:
   - Se abre la imagen desde la ruta  y se asegura de que esté en formato RGB.
   - Se convierte la imagen a un arreglo NumPy.
   - Se reorganiza la imagen en una matriz de forma (N, 3), donde cada fila representa un píxel (con sus valores R, G, B).
2) Inicialización de los centroides: Se eligen aleatoriamente k píxeles como los centroides iniciales.
3) Algoritmo K- Means: Se permite un máximo de 100 iteraciones para que los centroides se estabilicen.
   3.a) Se calcula la distancia  entre cada píxel y cada centroide, generando una matriz (N, k).
   3.b) Cada píxel se asigna al grupo del centroide más cercano.
   3.c)Se actualiza cada centroide como el promedio de los píxeles que le fueron asignados.
   Si un grupo queda vacío, se selecciona un nuevo píxel aleatorio.
   3.d) Si los centroides nuevos no difieren significativamente de los anteriores (atol=1), se considera que el algoritmo ha convergido y se termina antes de completar las 100 iteraciones.
4) Reemplazo de los colores de la imagen: Cada píxel es reemplazado por el color de su centroide asignado.
La matriz es reestructurada a su forma original (alto, ancho, 3) y convertida nuevamente en una imagen Pillow.
##COMENTARIOS 
- En el ingreso de datos durante la ejecución del script se controla que la ruta de la imagen sea válida y que el archivo exista mediante la ejecución del siguiente bloque de código:
  try:
    with open(ruta_imagen, 'rb'):
        pass #Continúa la ejecución del progama si encuentra a la imagen 
except FileNotFoundError:
    print("No se encontró la imagen. Por favor, verifique la ruta e intente nuevamente.")
    exit(1)  # Termina la ejecución del programa
Esto implementa un manejo de excepciones con un bloque try-except para verificar la existencia de la imagen. Si la ruta ingresada no es válida o el archivo no se encuentra, se captura la excepción FileNotFoundError y se informa al usuario, deteniendo el programa de forma controlada.
Luego, se controla mediante un bucle while  que el filtro seleccionado sea uno de los disponibles (halftone o kmeans), sin importar mayúsculas/minúsculas.
En el caso que el usuario seleccione el método K-Means  se controla por mismo método que  el valor ingresado para k  sea un número entero positivo, si el usuario no especifica, es  por default el valor 8. En el caso de Halftone se controla que el tamaño de los puntos sea un entero positivo y posee un valor por default un valor de 5. También, los ángulos para cada canal de color debe ser un string que luego se convierte en una lista, posee por deafult el valor "15,45,0". 

En caso de entradas inválidas, se informa al usuario con mensajes de error amigables y se solicita reingreso de los datos.
- Una vez finalizado el algoritmo de cuantización, ambos métodos retornan la imagen modificada, que se guarda y se muestra por pantalla. 
- El filtro K-Means posee un método de optimización para que realice el procedimiento en menos tiempo. 



