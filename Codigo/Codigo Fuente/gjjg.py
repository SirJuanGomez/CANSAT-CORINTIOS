import sys
import json
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy, QPushButton
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5.QtCore import Qt, QTimer

class GraphWidget(FigureCanvas):
    def __init__(self, title, ylabel, line_label, color='cyan', parent=None):
        fig, self.ax = plt.subplots()
        fig.patch.set_alpha(0.3)  # Fondo de la figura semitransparente
        fig.patch.set_facecolor('gray')  # Color de fondo con alpha
        
        super().__init__(fig)
        self.setParent(parent)
        
        # Añadir un cuadro con fondo al título
        self.ax.set_title(title, backgroundcolor="white", bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3', alpha=0.3))
        self.ax.set_xlabel("Tiempo (s)")  # Etiqueta del eje X
        self.ax.set_ylabel(ylabel)
        self.ax.grid(True, alpha=0.2)  # Hacer la cuadrícula más suave

        self.x_data = []
        self.y_data = []
        # Asignar el color de la línea
        self.line, = self.ax.plot([], [], label=line_label, color=color)  
        self.ax.legend(loc='upper right')  # La leyenda toma automáticamente el color de la línea
        self.ax.set_facecolor('none')  # Fondo del gráfico transparente
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 100)
        self.buffer_size = 100

    def update_graph(self, x, y):
        self.x_data.append(x)
        self.y_data.append(y)

        if len(self.x_data) > self.buffer_size:
            self.x_data = self.x_data[-self.buffer_size:]
            self.y_data = self.y_data[-self.buffer_size:]

        self.line.set_data(self.x_data, self.y_data)

        self.ax.set_xlim(max(0, self.x_data[-1] - 10), self.x_data[-1] + 1)
        self.ax.set_ylim(min(self.y_data) - 1, max(self.y_data) + 1)

        self.draw()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Sensor Data Dashboard')

        screen = QApplication.primaryScreen()
        screen_rect = screen.availableGeometry()
        screen_width = screen_rect.width()
        screen_height = screen_rect.height()

        self.setGeometry(0, 0, screen_width, screen_height)

        # Establecer imagen de fondo
        self.set_background_image('Imagenes/FondoMain.png')

        # Crear el layout principal
        main_layout = QHBoxLayout(self)

        # Frame izquierdo que ocupa el 85% (para las gráficas)
        self.frame_left = QFrame(self)
        self.frame_left.setFixedWidth(int(screen_width * 0.85))
        self.frame_left.setStyleSheet("background-color: transparent;")  # Fondo transparente
        left_layout = QVBoxLayout(self.frame_left)
        left_layout.setContentsMargins(0, 0, 0, 0)  # Quitar márgenes

        # Crear los gráficos para temperatura, altitud y presión con colores diferentes
        self.graph_temp = GraphWidget('Temperatura', 'Temperatura (°C)', 'Temperatura', 'black', self)
        self.graph_altitude = GraphWidget('Altitud', 'Altitud (m)', 'Altitud', 'white', self)
        self.graph_pressure = GraphWidget('Presión', 'Presión (hPa)', 'Presión', 'red', self)

        left_layout.addWidget(self.graph_temp)
        left_layout.addWidget(self.graph_altitude)
        left_layout.addWidget(self.graph_pressure)

        # Frame derecho que ocupa el 15% (para los valores de aceleración, giroscopio, UV y botón de cerrar)
        self.frame_right = QFrame(self)
        self.frame_right.setFixedWidth(int(screen_width * 0.15))
        self.frame_right.setStyleSheet("background-color: transparent;")
        right_layout = QVBoxLayout(self.frame_right)
        right_layout.setContentsMargins(0, 0, 0, 0)  # Quitar márgenes
        right_layout.setSpacing(10)  # Espacio entre los frames del 10%

        # Frame para los datos del giroscopio, acelerómetro y UV (70%)
        data_frame = QFrame(self.frame_right)
        data_frame.setStyleSheet("background-color: rgba(255, 255, 255, 0.3);")  # Fondo transparente
        data_layout = QVBoxLayout(data_frame)
        data_layout.setContentsMargins(0, 0, 0, 0)  # Quitar márgenes
        data_layout.setSpacing(10)  # Espacio entre los frames internos

        # Crear un frame para cada tipo de datos con sus valores debajo del nombre
        self.frames = {}
        labels = ['Aceleración X', 'Aceleración Y', 'Aceleración Z', 'Giroscopio X', 'Giroscopio Y', 'Giroscopio Z', 'Valor UV']
        for label_text in labels:
            frame = QFrame(data_frame)
            frame.setStyleSheet("background-color: transparent;")
            frame_layout = QVBoxLayout(frame)
            frame_layout.setContentsMargins(0, 0, 0, 0)  # Quitar márgenes

            name_label = QLabel(label_text)
            name_label.setAlignment(Qt.AlignCenter)
            name_label.setStyleSheet("color: black; background-color: transparent;")
            value_label = QLabel("0.00")
            value_label.setStyleSheet("color: black; background-color: transparent;")
            value_label.setAlignment(Qt.AlignCenter)
            frame_layout.addWidget(name_label)
            frame_layout.addWidget(value_label)
            frame_layout.setAlignment(Qt.AlignCenter)

            data_layout.addWidget(frame)
            self.frames[label_text] = value_label

        right_layout.addWidget(data_frame)

        # Agregar imagen sin rotar (5%)
        img_frame = QFrame(self.frame_right)
        img_frame.setFixedSize(124, 110)  # Ajusta el tamaño si es necesario
        img_layout = QVBoxLayout(img_frame)
        img_layout.setContentsMargins(0, 0, 0, 0)  # Quitar márgenes
        image_label = QLabel()
        pixmap = QPixmap('Imagenes/Main.png')
        image_label.setPixmap(pixmap.scaled(img_frame.size(), Qt.KeepAspectRatio))
        img_layout.addWidget(image_label)
        right_layout.addWidget(img_frame)

        # Agregar botón de cerrar con fondo difuminado
        close_button = QPushButton('Cerrar')
        close_button.clicked.connect(self.close)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0.3);  /* Negro con transparencia */
                color: white;
                border: none;  /* Sin borde */
                border-radius: 10px;  /* Borde redondeado */
                padding: 5px;
            }
            QPushButton:hover {
                background-color: rgba(255, 0, 0, 0.6);  /* Más opaco al pasar el ratón */
            }
        """)
        right_layout.addWidget(close_button)

        main_layout.addWidget(self.frame_left)
        main_layout.addWidget(self.frame_right)

        # Timer para actualizar los gráficos y datos (puedes ajustar el intervalo según sea necesario)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)  # Actualizar cada segundo

    def set_background_image(self, image_path):
        """Establecer la imagen de fondo."""
        palette = QPalette()
        pixmap = QPixmap(image_path)
        palette.setBrush(QPalette.Background, QBrush(pixmap))
        self.setPalette(palette)

    def update_data(self):
        """Actualizar datos de los gráficos y etiquetas."""
        # Aquí puedes leer datos de un archivo JSON o de otra fuente y actualizar los gráficos y las etiquetas
        # Ejemplo de actualización:
        # self.graph_temp.update_graph(time, temperature)
        # self.frames['Aceleración X'].setText(str(acc_x))
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())
