from PyQt5.QtWidgets import QApplication, QWidget, QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer
import sys
import json
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Sensor Data Dashboard')

        # Configuración de la ventana principal
        screen = QApplication.primaryScreen()
        screen_rect = screen.availableGeometry()
        screen_width = screen_rect.width()
        screen_height = screen_rect.height()
        self.setGeometry(0, 0, screen_width, screen_height)

        # Crear el layout principal
        main_layout = QHBoxLayout(self)

        # Frame izquierdo que ocupa el 85% (para las gráficas)
        self.frame_left = QFrame(self)
        self.frame_left.setFixedWidth(int(screen_width * 0.85))
        self.frame_left.setStyleSheet("background-color: #E0E0E0;")  # Color gris claro para el frame izquierdo

        # Crear layout vertical para el frame izquierdo
        left_layout = QVBoxLayout(self.frame_left)

        # Crear un frame centralizado para las gráficas
        self.frame_graphs = QFrame(self.frame_left)
        left_layout.addWidget(self.frame_graphs)
        
        # Layout vertical dentro del frame de gráficas
        graphs_layout = QVBoxLayout(self.frame_graphs)
        
        # Crear las 3 gráficas
        self.fig1, self.ax1 = plt.subplots()
        self.canvas1 = FigureCanvas(self.fig1)
        graphs_layout.addWidget(self.canvas1)

        self.fig2, self.ax2 = plt.subplots()
        self.canvas2 = FigureCanvas(self.fig2)
        graphs_layout.addWidget(self.canvas2)

        self.fig3, self.ax3 = plt.subplots()
        self.canvas3 = FigureCanvas(self.fig3)
        graphs_layout.addWidget(self.canvas3)

        # Frame derecho que ocupa el 15% (para el botón de cerrar y datos del giroscopio/UV)
        self.frame_right = QFrame(self)
        self.frame_right.setFixedWidth(int(screen_width * 0.15))
        self.frame_right.setStyleSheet("background-color: #B3E5FC;")  # Color azul claro para el frame derecho

        # Layout para organizar los tres frames en el lado derecho
        right_layout = QVBoxLayout(self.frame_right)

        # Frame superior para los valores de giroscopio, aceleración y UV (50% del frame derecho)
        self.frame_values = QFrame(self.frame_right)
        self.frame_values.setFixedHeight(int(screen_height * 0.50))
        self.frame_values.setStyleSheet("background-color: #C8E6C9;")  # Color verde claro para los valores
        values_layout = QVBoxLayout(self.frame_values)
        values_layout.setSpacing(10)  # Espacio entre los frames

        # Crear un layout para los valores en filas horizontales
        values_grid_layout = QVBoxLayout()
        values_grid_layout.setSpacing(10)

        # Frame para los valores de aceleración X
        self.frame_accel_x = QFrame(self.frame_values)
        self.frame_accel_x.setStyleSheet("background-color: #FFCCBC;")  # Color durazno para aceleración X
        accel_x_layout = QHBoxLayout(self.frame_accel_x)
        accel_x_layout.addWidget(QLabel('Aceleración X:', self.frame_accel_x))
        self.label_accel_x_value = QLabel('0', self.frame_accel_x)
        accel_x_layout.addWidget(self.label_accel_x_value)
        values_grid_layout.addWidget(self.frame_accel_x)

        # Frame para los valores de aceleración Y
        self.frame_accel_y = QFrame(self.frame_values)
        self.frame_accel_y.setStyleSheet("background-color: #FFAB91;")  # Color naranja claro para aceleración Y
        accel_y_layout = QHBoxLayout(self.frame_accel_y)
        accel_y_layout.addWidget(QLabel('Aceleración Y:', self.frame_accel_y))
        self.label_accel_y_value = QLabel('0', self.frame_accel_y)
        accel_y_layout.addWidget(self.label_accel_y_value)
        values_grid_layout.addWidget(self.frame_accel_y)

        # Frame para los valores de aceleración Z
        self.frame_accel_z = QFrame(self.frame_values)
        self.frame_accel_z.setStyleSheet("background-color: #FF8A80;")  # Color rojo claro para aceleración Z
        accel_z_layout = QHBoxLayout(self.frame_accel_z)
        accel_z_layout.addWidget(QLabel('Aceleración Z:', self.frame_accel_z))
        self.label_accel_z_value = QLabel('0', self.frame_accel_z)
        accel_z_layout.addWidget(self.label_accel_z_value)
        values_grid_layout.addWidget(self.frame_accel_z)

        # Frame para los valores del giroscopio X
        self.frame_gyro_x = QFrame(self.frame_values)
        self.frame_gyro_x.setStyleSheet("background-color: #D1C4E9;")  # Color morado claro para giroscopio X
        gyro_x_layout = QHBoxLayout(self.frame_gyro_x)
        gyro_x_layout.addWidget(QLabel('Giroscopio X:', self.frame_gyro_x))
        self.label_gyro_x_value = QLabel('0', self.frame_gyro_x)
        gyro_x_layout.addWidget(self.label_gyro_x_value)
        values_grid_layout.addWidget(self.frame_gyro_x)

        # Frame para los valores del giroscopio Y
        self.frame_gyro_y = QFrame(self.frame_values)
        self.frame_gyro_y.setStyleSheet("background-color: #D1C4E9;")  # Color morado claro para giroscopio Y
        gyro_y_layout = QHBoxLayout(self.frame_gyro_y)
        gyro_y_layout.addWidget(QLabel('Giroscopio Y:', self.frame_gyro_y))
        self.label_gyro_y_value = QLabel('0', self.frame_gyro_y)
        gyro_y_layout.addWidget(self.label_gyro_y_value)
        values_grid_layout.addWidget(self.frame_gyro_y)

        # Frame para los valores del giroscopio Z
        self.frame_gyro_z = QFrame(self.frame_values)
        self.frame_gyro_z.setStyleSheet("background-color: #D1C4E9;")  # Color morado claro para giroscopio Z
        gyro_z_layout = QHBoxLayout(self.frame_gyro_z)
        gyro_z_layout.addWidget(QLabel('Giroscopio Z:', self.frame_gyro_z))
        self.label_gyro_z_value = QLabel('0', self.frame_gyro_z)
        gyro_z_layout.addWidget(self.label_gyro_z_value)
        values_grid_layout.addWidget(self.frame_gyro_z)

        # Frame para el valor UV
        self.frame_uv = QFrame(self.frame_values)
        self.frame_uv.setStyleSheet("background-color: #B39DDB;")  # Color púrpura claro para UV
        uv_layout = QHBoxLayout(self.frame_uv)
        uv_layout.addWidget(QLabel('Valor UV:', self.frame_uv))
        self.label_uv_value = QLabel('0', self.frame_uv)
        uv_layout.addWidget(self.label_uv_value)
        values_grid_layout.addWidget(self.frame_uv)

        # Añadir el layout de valores al frame_values
        values_layout.addLayout(values_grid_layout)

        # Frame central para la imagen (30% del frame derecho)
        self.frame_image = QFrame(self.frame_right)
        self.frame_image.setFixedHeight(int(screen_height * 0.30))
        self.frame_image.setStyleSheet("background-color: #FFF59D;")  # Color amarillo claro para la imagen
        image_layout = QVBoxLayout(self.frame_image)
        
        # Cargar la imagen
        self.image_label = QLabel(self.frame_image)
        pixmap = QPixmap('Imagenes/Main.png')
        pixmap = pixmap.scaled(self.frame_image.size(), Qt.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)
        image_layout.addWidget(self.image_label)

        # Frame inferior para el botón de cerrar (20% del frame derecho)
        self.frame_button = QFrame(self.frame_right)
        self.frame_button.setFixedHeight(int(screen_height * 0.20))
        self.frame_button.setStyleSheet("background-color: #FFAB91;")  # Color naranja claro para el botón
        button_layout = QVBoxLayout(self.frame_button)

        # Botón para cerrar la ventana principal
        boton_cerrar = QPushButton('Cerrar', self)
        self.personalizar_boton(boton_cerrar)
        boton_cerrar.clicked.connect(self.cerrarVentana)
        button_layout.addWidget(boton_cerrar)

        # Añadir los frames al layout derecho
        right_layout.addWidget(self.frame_values)
        right_layout.addWidget(self.frame_image)
        right_layout.addWidget(self.frame_button)

        # Añadir los frames izquierdo y derecho al layout principal
        main_layout.addWidget(self.frame_left)
        main_layout.addWidget(self.frame_right)

        # Configuración de datos de ejemplo para las gráficas
        self.data_x = list(range(100))
        self.data_y1 = [0 for _ in range(100)]  # Inicializar con ceros
        self.data_y2 = [0 for _ in range(100)]  # Inicializar con ceros
        self.data_y3 = [0 for _ in range(100)]  # Inicializar con ceros

        # Temporizador para actualizar las gráficas
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)  # Actualizar cada segundo

    def personalizar_boton(self, boton):
            # Cambiar el texto del botón
            boton.setText("Cerrar")

            # Cambiar el tamaño del botón
            boton.setFixedSize(150, 50)

            # Cambiar la fuente del botón
            font = QFont("Arial", 12, QFont.Bold)
            boton.setFont(font)

            # Cambiar el color de fondo y el color del texto
            boton.setStyleSheet("""
                QPushButton {
                    background-color: #FF4C4C;  /* Rojo */
                    color: white;
                    border: 2px solid #B32D2D;  /* Rojo oscuro */
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #FF6C6C;  /* Rojo claro */
                }
                QPushButton:pressed {
                    background-color: #FF2C2C;  /* Rojo intenso */
                }
            """)

    def closeEvent(self, event):
             # Llamar a actualizarEstado cuando la ventana se está cerrando
            self.actualizarEstado()
            # Aceptar el evento de cierre para que la ventana se cierre
            event.accept()

    def actualizarEstado(self):
            ruta_archivo = 'Estados/estados.json'
            try:
            # Verificar si el archivo existe
                    if os.path.exists(ruta_archivo):
                        with open(ruta_archivo, 'r') as file:
                            # Leer el contenido del archivo
                            data = json.load(file)

                        # Verificar si el contenido es una lista con al menos un diccionario
                        if isinstance(data, list) and len(data) > 0:
                            # Actualizar los valores de 'run', 'serial' y 'graficas' a 0
                            data[0]['run'] = 0
                            data[0]['serial'] = 0
                            data[0]['graficas'] = 0
                            
                            # Guardar los cambios de vuelta en el archivo
                            with open(ruta_archivo, 'w') as file:
                                json.dump(data, file, indent=4)  # Usar indentación para mejor legibilidad
            except Exception as e:
                    print(f"Error al actualizar el estado: {e}")
    def cerrarVentana(self):
                # Llamar a actualizarEstado antes de cerrar la ventana
                self.actualizarEstado()
                self.close()

    def update_data(self):
        try:
            # Leer los datos del archivo JSON
            with open('sensor_data.json', 'r') as file:
                data = json.load(file)
            
            # Obtener el último registro
            if isinstance(data, list) and len(data) > 0 and isinstance(data[-1], dict):
                last_entry = data[-1]
                accel_x = last_entry.get('ax', 0)
                accel_y = last_entry.get('ay', 0)
                accel_z = last_entry.get('az', 0)
                gyro_x = last_entry.get('gx', 0)
                gyro_y = last_entry.get('gy', 0)
                gyro_z = last_entry.get('gz', 0)
                uv_value = last_entry.get('uvValue', 0)

                # Actualizar los valores de las etiquetas
                self.label_accel_x_value.setText(f'{accel_x:.2f}')
                self.label_accel_y_value.setText(f'{accel_y:.2f}')
                self.label_accel_z_value.setText(f'{accel_z:.2f}')
                self.label_gyro_x_value.setText(f'{gyro_x:.2f}')
                self.label_gyro_y_value.setText(f'{gyro_y:.2f}')
                self.label_gyro_z_value.setText(f'{gyro_z:.2f}')
                self.label_uv_value.setText(f'{uv_value:.2f}')

                # Actualizar los datos de las gráficas
                self.data_x.append(self.data_x[-1] + 1)
                self.data_x.pop(0)

                self.data_y1.append(accel_x)
                self.data_y1.pop(0)

                self.data_y2.append(accel_y)
                self.data_y2.pop(0)

                self.data_y3.append(accel_z)
                self.data_y3.pop(0)

                # Limpiar las gráficas
                self.ax1.clear()
                self.ax2.clear()
                self.ax3.clear()

                # Dibujar las gráficas con los nuevos datos
                self.ax1.plot(self.data_x, self.data_y1, label="Temperatura", color='red')
                self.ax2.plot(self.data_x, self.data_y2, label="Presión", color='blue')
                self.ax3.plot(self.data_x, self.data_y3, label="Altitud", color='green')

                # Añadir nombres a los ejes y cuadrículas
                self.ax1.set_xlabel('Tiempo')
                self.ax1.set_ylabel('Temperatura (°C)')
                self.ax1.grid(True)

                self.ax2.set_xlabel('Tiempo')
                self.ax2.set_ylabel('Presión (hPa)')
                self.ax2.grid(True)

                self.ax3.set_xlabel('Tiempo')
                self.ax3.set_ylabel('Altitud (m)')
                self.ax3.grid(True)

                # Actualizar los lienzos
                self.canvas1.draw()
                self.canvas2.draw()
                self.canvas3.draw()

        except Exception as e:
            print(f'Error al leer datos del archivo JSON: {e}')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())
