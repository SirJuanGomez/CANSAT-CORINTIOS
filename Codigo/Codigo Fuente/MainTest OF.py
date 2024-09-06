import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import subprocess
import os

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
    update_status(0)
    
    root.destroy()

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

def main():
    global root
    # Crear la ventana principal
    root = tk.Tk()
    root.title("Iniciar Scripts")

    # Configurar la ventana para que use el tamaño completo de la pantalla
    root.state('zoomed')

    # Crear un contenedor para la imagen de fondo
    fondo_frame = tk.Frame(root)
    fondo_frame.place(relwidth=1, relheight=1)

    # Cargar la imagen de fondo
    try:
        # Ruta de la imagen de fondo
        image_path = os.path.join(os.getcwd(), 'Imagenes', 'FondoMain.png')
        
        # Abrir la imagen y redimensionarla para ajustarse al tamaño de la ventana manteniendo su proporción
        imagen = Image.open(image_path)
        imagen = resize_image(imagen, root.winfo_screenwidth(), root.winfo_screenheight())
        imagen_tk = ImageTk.PhotoImage(imagen)
        
        # Crear un Label para mostrar la imagen de fondo
        fondo_label = tk.Label(fondo_frame, image=imagen_tk)
        fondo_label.place(relwidth=1, relheight=1)
        fondo_label.image = imagen_tk  # Mantener una referencia a la imagen
    except Exception as e:
        print(f"Error al cargar la imagen de fondo: {e}")

    # Crear un Frame para el botón con tamaño fijo
    button_frame = tk.Frame(root, width=360, height=360, bg='#153553')
    button_frame.place(relx=0.5, rely=0.5, anchor='center')  # Centrar el frame en la ventana

    # Cargar la imagen del título
    try:
        # Ruta de la imagen del título
        title_image_path = os.path.join(os.getcwd(), 'Imagenes', 'Main.png')
        title_image = Image.open(title_image_path)
        title_image = resize_image(title_image, 360, 100)  # Ajustar el tamaño según sea necesario
        title_image_tk = ImageTk.PhotoImage(title_image)
        
        # Crear un Label para mostrar la imagen del título
        title_label = tk.Label(button_frame, image=title_image_tk, bg='#153553')
        title_label.pack(pady=(0, 10))  # Espacio entre la imagen del título y el botón
        title_label.image = title_image_tk  # Mantener una referencia a la imagen
    except Exception as e:
        print(f"Error al cargar la imagen del título: {e}")

    # Crear un estilo ttk
    style = ttk.Style()
    style.configure('TCenter', font=('Helvetica', 20))

    # Crear un botón para iniciar los scripts
    button = ttk.Button(button_frame, text="Iniciar", command=start_scripts)
    button.pack(expand=True, pady=20)  # Expandir y añadir un margen de 20 píxeles en el eje Y

    # Configurar el manejador para el cierre de la ventana
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Ejecutar el bucle principal de la aplicación
    root.mainloop()

if __name__ == "__main__":
    main()
