import tkinter as tk
from tkinter import ttk
import subprocess
import os
import signal

# Variables globales para mantener las referencias a los procesos
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
    
    # Cerrar la ventana actual
    root.destroy()

def on_closing():
    global processes
    for proc in processes:
        proc.terminate()  # Terminar el proceso
        proc.wait()       # Esperar a que el proceso termine
    
    # Actualizar el archivo de estado
    update_status(False)
    
    root.destroy()

def main():
    global root
    # Crear la ventana principal
    root = tk.Tk()
    root.title("Iniciar Scripts")

    # Configurar la ventana para que use el tamaño completo de la pantalla
    root.state('zoomed')

    # Crear un estilo ttk
    style = ttk.Style()
    style.configure('TCenter', font=('Helvetica', 70))

    # Crear un botón para iniciar los scripts
    button = ttk.Button(root, text="Iniciar", command=start_scripts)
    button.pack(pady=20)  # Añadir un margen de 20 píxeles en el eje Y

    # Configurar el manejador para el cierre de la ventana
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Ejecutar el bucle principal de la aplicación
    root.mainloop()

if __name__ == "__main__":
    main()
