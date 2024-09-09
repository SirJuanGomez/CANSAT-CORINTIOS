import sys
import json
import os
from PyQt5.QtWidgets import QApplication, QWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtCore import QTimer, Qt
import pyqtgraph as pg

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Sensor Data Dashboard')

        screen = QApplication.primaryScreen()
        screen_rect = screen.availableGeometry()
        screen_width = screen_rect.width()
        screen_height = screen_rect.height()

        self.setGeometry(0, 0, screen_width, screen_height)

        # Verificar si el valor run es 1
        if not self.check_run_status():
            QMessageBox.critical(self, "Error", "El valor de 'run' no es 1. La aplicación se cerrará.")
            sys.exit()

        # Crear el layout principal
        main_layout = QHBoxLayout(self)

        # Frame izquierdo que ocupa el 90% (para las gráficas)
        self.frame_left = QFrame(self)
        self.frame_left.setFixedWidth(int(screen_width * 0.85))
        left_layout = QVBoxLayout(self.frame_left)

        # Agregar un marco alrededor de las gráficas
        self.graph_container = QFrame(self.frame_left)
        self.graph_container.setStyleSheet("border: 2px solid black; padding: 10px;")
        graph_layout = QVBoxLayout(self.graph_container)
        
        # Crear los gráficos con diseño mejorado
        self.graph_temp = pg.PlotWidget(title='Temperatura')
        self.graph_altitude = pg.PlotWidget(title='Altitud')
        self.graph_pressure = pg.PlotWidget(title='Presión')

        # Configuración de los gráficos
        self.setup_graph(self.graph_temp, 'Temperatura (°C)', 'Índice')
        self.setup_graph(self.graph_altitude, 'Altitud (m)', 'Índice')
        self.setup_graph(self.graph_pressure, 'Presión (hPa)', 'Índice')

        graph_layout.addWidget(self.graph_temp)
        graph_layout.addWidget(self.graph_altitude)
        graph_layout.addWidget(self.graph_pressure)

        left_layout.addWidget(self.graph_container)

        # Frame derecho que ocupa el 10% (para los valores de aceleración, giroscopio, UV y botón de cerrar)
        self.frame_right = QFrame(self)
        self.frame_right.setFixedWidth(int(screen_width * 0.10))
        right_layout = QVBoxLayout(self.frame_right)

        # Agregar imagen rotada (5%)
        img_frame = QFrame(self.frame_right)
        img_frame.setFixedSize(124, 110)
        image_label = QLabel()
        pixmap = QPixmap('Imagenes/Main.png')
        rotated_pixmap = pixmap.transformed(QTransform().rotate(90))
        image_label.setPixmap(rotated_pixmap.scaled(img_frame.size(), Qt.KeepAspectRatio))
        right_layout.addWidget(image_label)

        # Agregar valores de aceleración, giroscopio y UV
        self.create_sensor_values_frame(right_layout)

        # Botón para abrir la ventana de gráficas
        boton_abrir_graficas = QPushButton('Abrir Ventana de Gráficas', self)
        boton_abrir_graficas.clicked.connect(self.abrirVentanaGraficas)
        right_layout.addWidget(boton_abrir_graficas)

        # Botón para cerrar la ventana principal
        boton_cerrar = QPushButton('Cerrar Ventana Principal', self)
        boton_cerrar.clicked.connect(self.cerrarVentana)
        right_layout.addWidget(boton_cerrar)

        main_layout.addWidget(self.frame_left)
        main_layout.addWidget(self.frame_right)

        # Temporizador para actualización de datos
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)  # Actualiza cada segundo

        # Variables para almacenar los datos de los gráficos
        self.data_temp = []
        self.data_altitude = []
        self.data_pressure = []

        # Configuración inicial de los gráficos para evitar acumulación de datos
        self.max_points = 100

    def setup_graph(self, graph, y_label, x_label):
        graph.setLabel('left', y_label)
        graph.setLabel('bottom', x_label)
        graph.showGrid(x=True, y=True)
        graph.addLegend()
        graph.setLabel('left', 'Valor', color='black', size='12pt')
        graph.setLabel('bottom', 'Índice', color='black', size='12pt')

    def update_data(self):
        ruta_archivo = 'sensor_data.json'

        try:
            with open(ruta_archivo, 'r') as file:
                data = json.load(file)

            if data:
                # Usar el índice como valor para el eje X
                x = list(range(len(data)))
                temperatures = [entry.get('temperature', 0) for entry in data]
                altitudes = [entry.get('altitude', 0) for entry in data]
                pressures = [entry.get('pressure', 0) for entry in data]
                accelerations = [entry.get('ax', 0), entry.get('ay', 0), entry.get('az', 0)]
                gyros = [entry.get('gx', 0), entry.get('gy', 0), entry.get('gz', 0)]
                uv_value = entry.get('uvValue', 0)

                # Actualizar los datos, manteniendo solo los últimos max_points puntos
                self.data_temp = list(zip(x, temperatures))[-self.max_points:]
                self.data_altitude = list(zip(x, altitudes))[-self.max_points:]
                self.data_pressure = list(zip(x, pressures))[-self.max_points:]

                # Limpiar y actualizar los gráficos
                self.graph_temp.clear()
                self.graph_temp.plot(*zip(*self.data_temp), pen='b', name='Temperatura')
                self.graph_altitude.clear()
                self.graph_altitude.plot(*zip(*self.data_altitude), pen='g', name='Altitud')
                self.graph_pressure.clear()
                self.graph_pressure.plot(*zip(*self.data_pressure), pen='r', name='Presión')

                # Actualizar los valores en el frame derecho
                self.update_sensor_values(accelerations, gyros, uv_value)

        except Exception as e:
            print(f"Error al actualizar los datos: {e}")

    def create_sensor_values_frame(self, layout):
        # Crear y agregar los valores de aceleración, giroscopio y UV al frame derecho
        self.sensor_values_frame = QFrame(self)
        self.sensor_values_frame.setStyleSheet("border: 1px solid black; padding: 5px;")
        sensor_layout = QVBoxLayout(self.sensor_values_frame)

        # Aceleración
        self.accel_labels = {
            'ax': QLabel('ax: 0'),
            'ay': QLabel('ay: 0'),
            'az': QLabel('az: 0')
        }
        for label in self.accel_labels.values():
            sensor_layout.addWidget(label)

        # Giroscopio
        self.gyro_labels = {
            'gx': QLabel('gx: 0'),
            'gy': QLabel('gy: 0'),
            'gz': QLabel('gz: 0')
        }
        for label in self.gyro_labels.values():
            sensor_layout.addWidget(label)

        # UV
        self.uv_label = QLabel('UV: 0')
        sensor_layout.addWidget(self.uv_label)

        layout.addWidget(self.sensor_values_frame)

    def update_sensor_values(self, accelerations, gyros, uv_value):
        # Actualizar las etiquetas de los valores de aceleración, giroscopio y UV
        self.accel_labels['ax'].setText(f'ax: {accelerations[0]}')
        self.accel_labels['ay'].setText(f'ay: {accelerations[1]}')
        self.accel_labels['az'].setText(f'az: {accelerations[2]}')

        self.gyro_labels['gx'].setText(f'gx: {gyros[0]}')
        self.gyro_labels['gy'].setText(f'gy: {gyros[1]}')
        self.gyro_labels['gz'].setText(f'gz: {gyros[2]}')

        self.uv_label.setText(f'UV: {uv_value}')

    def check_run_status(self):
        ruta_archivo = 'Estados/estados.json'
        if not os.path.exists(ruta_archivo):
            return False

        try:
            with open(ruta_archivo, 'r') as file:
                data = json.load(file)
                if isinstance(data, list) and len(data) > 0:
                    return data[0].get('run', 0) == 1
        except Exception as e:
            print(f"Error al leer el archivo de estados: {e}")

        return False

    def abrirVentanaGraficas(self):
        self.ventana_graficas = VentanaGraficas()
        self.ventana_graficas.show()

    def closeEvent(self, event):
        self.actualizarEstado()
        event.accept()

    def actualizarEstado(self):
        ruta_archivo = 'Estados/estados.json'
        try:
            if os.path.exists(ruta_archivo):
                with open(ruta_archivo, 'r') as file:
                    data = json.load(file)

                if isinstance(data, list) and len(data) > 0:
                    data[0]['run'] = 0  # Actualizar el estado a 0
                    with open(ruta_archivo, 'w') as file:
                        json.dump(data, file)
        except Exception as e:
            print(f"Error al actualizar el estado: {e}")

    def cerrarVentana(self):
        self.close()

class VentanaGraficas(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Ventana de Gráficas')

        # Configuración inicial de la ventana de gráficas
        self.setGeometry(100, 100, 800, 600)
        layout = QVBoxLayout(self)

        # Agregar gráficos a la ventana
        self.graph_temp = pg.PlotWidget(title='Temperatura')
        self.graph_altitude = pg.PlotWidget(title='Altitud')
        self.graph_pressure = pg.PlotWidget(title='Presión')

        self.setup_graph(self.graph_temp, 'Temperatura (°C)', 'Índice')
        self.setup_graph(self.graph_altitude, 'Altitud (m)', 'Índice')
        self.setup_graph(self.graph_pressure, 'Presión (hPa)', 'Índice')

        layout.addWidget(self.graph_temp)
        layout.addWidget(self.graph_altitude)
        layout.addWidget(self.graph_pressure)

        # Temporizador para actualización de datos
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)  # Actualiza cada segundo

        # Variables para almacenar los datos de los gráficos
        self.data_temp = []
        self.data_altitude = []
        self.data_pressure = []
        self.max_points = 100

    def setup_graph(self, graph, y_label, x_label):
        graph.setLabel('left', y_label)
        graph.setLabel('bottom', x_label)
        graph.showGrid(x=True, y=True)
        graph.addLegend()
        graph.setLabel('left', 'Valor', color='black', size='12pt')
        graph.setLabel('bottom', 'Índice', color='black', size='12pt')

    def update_data(self):
        ruta_archivo = 'sensor_data.json'

        try:
            with open(ruta_archivo, 'r') as file:
                data = json.load(file)

            if data:
                # Usar el índice como valor para el eje X
                x = list(range(len(data)))
                temperatures = [entry.get('temperature', 0) for entry in data]
                altitudes = [entry.get('altitude', 0) for entry in data]
                pressures = [entry.get('pressure', 0) for entry in data]

                # Actualizar los datos, manteniendo solo los últimos max_points puntos
                self.data_temp = list(zip(x, temperatures))[-self.max_points:]
                self.data_altitude = list(zip(x, altitudes))[-self.max_points:]
                self.data_pressure = list(zip(x, pressures))[-self.max_points:]

                # Limpiar y actualizar los gráficos
                self.graph_temp.clear()
                self.graph_temp.plot(*zip(*self.data_temp), pen='b', name='Temperatura')
                self.graph_altitude.clear()
                self.graph_altitude.plot(*zip(*self.data_altitude), pen='g', name='Altitud')
                self.graph_pressure.clear()
                self.graph_pressure.plot(*zip(*self.data_pressure), pen='r', name='Presión')

        except Exception as e:
            print(f"Error al actualizar los datos en la ventana de gráficas: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.showMaximized()
    sys.exit(app.exec_())
