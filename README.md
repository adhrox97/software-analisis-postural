# software-analisis-postural
El software construido para la tesis titulada "Desarrollo de un sistema para el análisis postural 
en centros de acondicionamiento físico utilizando visión por computador" contenido en el archivo 
llamado "FinalVersion.rar" requiere la versión de python 2.7 y está segmentado en 7 archivos PY los 
cuales corresponden a:

MainWindow.py = Codigo principal

Funciones.py = Funciones para los procesos utilizados en el código principal

Base_Datos.py = Manejo de las funciones y arquitecturas utilizadas en el almacenamiento de datos

detect_hsv.py = Codigo modificado para facilitar la obtencion de los rangos de deteccion para el 
espacio de color HSV

mplwidget.py = Configuracion inicial de la grafica embebida utilizada para la visualizacion de datos
de profundidad obtenidas en la ultima medicion de un paciente

mplwidget1.py = Configuracion inicial de la grafica embebida utilizada para la visualizacion de datos
de profundidad entre 3 fechas distintas de un paciente

mplwidget2.py = Configuracion inicial de la grafica embebida utilizada para la comparacion de los 
angulos medidos entre maximo 10 fechas distintas de un paciente

Entre otros archivos importantes como:

personas = archivo base de datos

archivos svg,jpg,png = iconos e imagenes utilizadas para la interfaz

mainWindow.ui = Almacena datos de la configuración de la interfaz de usuario (Qt Designer)

Se requieren las siguientes librerias:

-PyQt5 (dado a incompatibilidad en la version python 2.7 se ha instalado una modificacion por medio 
de https://github.com/pyqt/python-qt5)
-numpy
-pygame
-pykinect
-cv2(open cv)
-qimage2ndarray
-matplotlib
-sqlite3
-skimage
-trimesh
-stl
-pyglet(v 1.4.10)
-pyrender(Esta libreria se ha modificado, dado a esto se adjunta el archivo "pyrender.rar" en la 
presente carpeta. La carpeta una vez descomprimida, debe ser copiada o reemplazada en la carpeta de
python\Lib\site-packages)
