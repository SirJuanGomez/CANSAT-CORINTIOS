import sys
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PIL import Image

# Variables globales para los procesos
processes = []
status_file = 'status.txt'

def update_status(value):
    """Actualiza el archivo de estado con el valor dado (0 o 1)."""
    with open(status_file, 'w') as f:
        f.write(str(value))

def start_scripts():
    global processes
    # Rutas a los archivos scripts
    script1_path = os.path.join(os.getcwd(), 'serialtest.py')
    script2_path = os.path.join(os.getcwd(), 'testwindows(true).py')
    
    # Ejecutar ambos scripts en nuevos procesos
    processes.append(subprocess.Popen(['python', script1_path]))
    processes.append(subprocess.Popen(['python', script2_path]))
    
    # Actualizar el archivo de estado
    update_status(1)

def on_closing():
    global processes
    for proc in processes:
        proc.terminate()  # Terminar los procesos
        proc.wait()       # Esperar a que terminen
    
    # Actualizar el archivo de estado
    update_status(0)

def resize_image(image, max_width, max_height):
    """Redimensiona la imagen manteniendo su proporción."""
    width, height = image.size
    aspect_ratio = width / height
    
    if width > height:
        new_width = min(max_width, width)
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = min(max_height, height)
        new_width = int(new_height * aspect_ratio)
    
    return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Iniciar Scripts")
        self.setGeometry(100, 100, 800, 600)  # Puedes ajustar el tamaño según sea necesario
        self.setWindowState(Qt.WindowMaximized)  # Ventana en pantalla completa

        # Crear un contenedor principal
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        # Layout para la ventana
        layout = QVBoxLayout(main_widget)
        layout.setAlignment(Qt.AlignCenter)  # Centrar el contenido

        # Imagen de fondo
        try:
            image_path = os.path.join(os.getcwd(), 'Imagenes', 'FondoMain.png')
            imagen = Image.open(image_path)
            imagen = resize_image(imagen, self.width(), self.height())
            imagen.save('resized_image.png')  # Guardar la imagen redimensionada temporalmente
            fondo_pixmap = QPixmap('resized_image.png')

            fondo_label = QLabel(self)
            fondo_label.setPixmap(fondo_pixmap)
            fondo_label.setScaledContents(True)
            fondo_label.setGeometry(0, 0, self.width(), self.height())  # Asegurar que la imagen cubra toda la ventana
            fondo_label.lower()  # Enviar el fondo al nivel más bajo
        except Exception as e:
            print(f"Error al cargar la imagen de fondo: {e}")

        # Frame para el botón
        button_frame = QFrame(self)
        button_frame.setFixedSize(360, 360)
        button_frame.setStyleSheet("background-color: #153553; border-radius: 10px;")
        layout.addWidget(button_frame, alignment=Qt.AlignCenter)

        # Imagen del título en el frame
        try:
            title_image_path = os.path.join(os.getcwd(), 'Imagenes', 'Main.png')
            title_image = Image.open(title_image_path)
            title_image = resize_image(title_image, 360, 100)
            title_image.save('resized_title.png')  # Guardar la imagen redimensionada temporalmente
            title_pixmap = QPixmap('resized_title.png')

            title_label = QLabel(button_frame)
            title_label.setPixmap(title_pixmap)
            title_label.setAlignment(Qt.AlignCenter)
            title_label.setStyleSheet("background-color: #153553;")
            title_label.move(80, 50)
        except Exception as e:
            print(f"Error al cargar la imagen del título: {e}")

        # Botón para iniciar los scripts
        button = QPushButton("Iniciar", button_frame)
        button.setFixedSize(200, 100)
        button.move(80, 200)  # Centrar el botón dentro del frame
        button.clicked.connect(start_scripts)  # Conectar el botón con la función de iniciar scripts

    def closeEvent(self, event):
        on_closing()  # Llamar a la función para terminar procesos al cerrar
        event.accept()  # Aceptar el cierre

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
