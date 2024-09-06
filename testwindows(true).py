import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QHBoxLayout, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configura la ventana principal
        self.setWindowTitle('Ventana con tres Frames')
        self.resize(800, 600)  # Tamaño inicial de la ventana

        # Crea un widget central y un layout horizontal
        central_widget = QWidget()
        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)  # Elimina los márgenes del layout
        layout.setSpacing(0)  # Elimina el espacio entre los frames
        self.setCentralWidget(central_widget)

        # Crea el primer QFrame (70% del ancho de la ventana)
        self.frame1 = QFrame()
        self.frame1.setStyleSheet("background-color: lightblue;")
        layout.addWidget(self.frame1, 7)  # Establece el factor de estiramiento en 7

        # Crea el contenedor para los frames de 25% y 5%
        self.frame2_container = QFrame()
        self.frame2_container.setStyleSheet("background-color: lightgray;")
        self.frame2_container_layout = QVBoxLayout(self.frame2_container)
        self.frame2_container_layout.setContentsMargins(0, 0, 0, 0)
        self.frame2_container_layout.setSpacing(0)

        # Crea el frame restante (25% del ancho de la ventana menos el 5%)
        self.frame2 = QFrame()
        self.frame2.setStyleSheet("background-color: lightgreen;")
        self.frame2_container_layout.addWidget(self.frame2)  # Agrega el frame2 en la parte superior

        # Crea el frame de 5% del ancho de la ventana
        self.frame3 = QFrame()
        self.frame3.setStyleSheet("background-color: lightcoral;")
        self.frame2_container_layout.addWidget(self.frame3)  # Agrega el frame3 en la parte inferior

        layout.addWidget(self.frame2_container, 3)  # Establece el factor de estiramiento en 3 para el contenedor

        self.setLayout(layout)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Ajusta la altura del frame3 cuando la ventana cambia de tamaño
        self.frame3.setFixedHeight(int(self.height() * 0.05))
        self.frame2.setFixedHeight(self.height() - self.frame3.height())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()  # Muestra la ventana en modo maximizado
    sys.exit(app.exec_())
