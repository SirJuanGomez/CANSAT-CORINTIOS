import sys
import subprocess
import json
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Window')

        # Configurar el tamaño y el layout de la ventana
        self.setGeometry(100, 100, 800, 600)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Botón para abrir las ventanas de gráficos y serial
        open_graphics_and_serial_button = QPushButton('Iniciar Gráficas y Serial')
        open_graphics_and_serial_button.clicked.connect(self.open_graphics_and_serial)
        layout.addWidget(open_graphics_and_serial_button)

    def open_graphics_and_serial(self):
        # Ejecutar graficas.py
        subprocess.Popen(['python', 'graficas.py'])

        # Ejecutar serialtest.py
        subprocess.Popen(['python', 'datosg.py'])

        # Actualizar el archivo estados.json
        self.update_status_file()

        # Cerrar la ventana principal
        self.close()

    def update_status_file(self):
        estados_path = 'Estados/estados.json'
        # Verificar si el archivo existe
        if not os.path.exists(estados_path):
            # Crear el archivo con valores iniciales si no existe
            with open(estados_path, 'w') as file:
                json.dump([{"run": 0, "serial": 0, "graficas": 0}], file)

        try:
            with open(estados_path, 'r+') as file:
                # Leer los datos actuales
                data = json.load(file)

                if isinstance(data, list) and len(data) > 0:
                    # Modificar los valores
                    data[0]['run'] = 1
                    data[0]['serial'] = 1
                    data[0]['graficas'] = 1

                    # Volver al principio del archivo para sobrescribir
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
    window.show()
    sys.exit(app.exec_())
