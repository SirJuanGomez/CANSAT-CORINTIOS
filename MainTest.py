import sys
import subprocess
import json
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFrame, QLabel, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QPalette, QBrush

class BackgroundWidget(QWidget):
    def __init__(self, image_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_path = image_path
        self.pixmap = QPixmap(self.image_path)
        
        if self.pixmap.isNull():
            print(f"No se pudo cargar la imagen de fondo desde {self.image_path}")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap)

    def resizeEvent(self, event):
        self.pixmap = self.pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        super().resizeEvent(event)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Window')

        # Flag para controlar la actualización del JSON
        self.update_json_on_close = False

        # Configurar el tamaño y el layout de la ventana
        self.setGeometry(100, 100, 800, 600)

        # Crear un widget personalizado para el fondo
        self.background_widget = BackgroundWidget('Imagenes/FondoMain.png')
        self.background_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCentralWidget(self.background_widget)
        
        # Crear un layout que centrará el QFrame
        central_layout = QVBoxLayout(self.background_widget)
        central_layout.setContentsMargins(0, 0, 0, 0)  # Eliminar márgenes del layout
        central_layout.setSpacing(0)  # Eliminar el espacio entre widgets
        central_layout.setAlignment(Qt.AlignCenter)

        # Crear un QFrame centrado que estará sobre el fondo
        self.frame = QFrame(self.background_widget)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setLineWidth(2)
        self.frame.setStyleSheet('background-color: transparent;')  # Fondo blanco semitransparente
        self.frame.setFixedSize(400, 300)  # Ajustar el tamaño del frame

        # Crear el layout para el QFrame
        frame_layout = QVBoxLayout(self.frame)
        frame_layout.setContentsMargins(10, 10, 10, 10)  # Márgenes internos del frame
        frame_layout.setAlignment(Qt.AlignCenter)

        # Añadir imagen al QFrame
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.load_image('Imagenes/Main.png')  # Ruta de la imagen
        self.image_label.setStyleSheet('background-color: transparent;')
        frame_layout.addWidget(self.image_label)

        # Botón personalizado para abrir las ventanas de gráficos y serial
        open_graphics_and_serial_button = QPushButton('Iniciar Gráficas y Serial')
        open_graphics_and_serial_button.setStyleSheet(""" 
            QPushButton {
                background-color: #4CAF50; /* Verde */ 
                border: 1px;                                
                color: white; 
                padding: 10px 20px; 
                font-size: 16px; 
                border-radius: 8px; /* Bordes redondeados */ 
            } 
            QPushButton:hover { 
                background-color: #D4AF37; /* Verde más oscuro */ 
            } 
        """)
        open_graphics_and_serial_button.clicked.connect(self.open_graphics_and_serial)
        frame_layout.addWidget(open_graphics_and_serial_button)

        # Añadir el frame al layout principal
        central_layout.addWidget(self.frame, Qt.AlignCenter)

    def load_image(self, path):
        pixmap = QPixmap(path)
        if not pixmap.isNull():
            self.image_label.setPixmap(pixmap.scaled(400, 300, Qt.KeepAspectRatio))  # Ajustar el tamaño según sea necesario
        else:
            print(f"No se pudo cargar la imagen desde {path}")

    def open_graphics_and_serial(self):
        # Ejecutar graficas.py y datosg.py
        try:
            subprocess.run(['python', 'graficas.py'], check=True)
            subprocess.run(['python', 'datosg.py'], check=True)
            self.update_json_on_close = True  # Solo actualizar el JSON si se ejecutaron los scripts correctamente
        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar los scripts: {e}")
        
        # Cerrar la ventana principal
        self.close()

    def closeEvent(self, event):
        # Actualizar el archivo estados.json solo si el flag está activado
        if self.update_json_on_close:
            self.update_status_file()
        super().closeEvent(event)

    def update_status_file(self):
        estados_path = 'Estados/estados.json'
        
        # Verificar si el archivo existe y crear si es necesario
        if not os.path.exists(estados_path):
            with open(estados_path, 'w') as file:
                json.dump([{"run": 0, "serial": 0, "graficas": 0}], file)
        
        # Leer y actualizar el archivo JSON
        try:
            with open(estados_path, 'r+') as file:
                data = json.load(file)

                if isinstance(data, list) and len(data) > 0:
                    # Modificar los valores
                    data[0]['run'] = 1
                    data[0]['serial'] = 1
                    data[0]['graficas'] = 1

                    # Volver al principio del archivo y sobrescribir
                    file.seek(0)
                    json.dump(data, file)
                    file.truncate()  # Eliminar cualquier dato restante después del nuevo contenido
                else:
                    raise ValueError("El archivo estados.json no contiene una lista válida o está vacío.")
        except (ValueError, json.JSONDecodeError) as e:
            print(f"Error al leer o escribir el archivo estados.json: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())
