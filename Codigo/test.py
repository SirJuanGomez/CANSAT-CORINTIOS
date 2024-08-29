import tkinter as tk
from tkinter import PhotoImage, ttk
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Definir la ruta a la carpeta 'imagenes'
ruta_Imagenes = os.path.join(os.path.dirname(__file__), 'imagenes')

# Definir las rutas a las imágenes
ruta_fondo_main = os.path.join(ruta_Imagenes, 'FondoMain.png')
ruta_imagen = os.path.join(ruta_Imagenes, 'Main.png')

# Variables globales para almacenar datos
tiempos = []
temperaturas = []
presiones = []
altitudes = []
canvas = [None] * 3
ax = [None] * 3
fig = [None] * 3

def mostrar_nueva_interfaz():
    """Crea y muestra la nueva interfaz con 3 cuadros en una línea recta, centrados y con tamaño fijo."""
    global canvas, ax, fig  # Declarar como globales para usarlas en la función
    nueva_ventana = tk.Toplevel(root)
    nueva_ventana.title("CANSAT CORINTIOS")

    # Obtener tamaño de pantalla
    pantalla_ancho = nueva_ventana.winfo_screenwidth()
    pantalla_alto = nueva_ventana.winfo_screenheight()

    # Ajustar el tamaño de la ventana nueva para que ocupe toda la pantalla
    nueva_ventana.geometry(f"{pantalla_ancho}x{pantalla_alto}")

    # Crear un Label para la imagen de fondo
    try:
        fondo_imagen = PhotoImage(file=ruta_fondo_main)
        fondo_label = tk.Label(nueva_ventana, image=fondo_imagen)
        fondo_label.place(relwidth=1, relheight=1)
    except Exception as e:
        print(f"Error al cargar la imagen de fondo: {e}")

    # Crear un contenedor para centrar los cuadros
    contenedor = tk.Frame(nueva_ventana, bg='white')
    contenedor.place(relx=0.5, rely=0.5, anchor='center')

    # Crear un marco para cada gráfico
    for i in range(3):
        fig[i], ax[i] = plt.subplots(figsize=(6, 6), dpi=100)  # El tamaño del gráfico en pulgadas
        ax[i].set_title(["Temperatura vs Tiempo", "Presión vs Tiempo", "Altitud vs Tiempo"][i])
        canvas[i] = FigureCanvasTkAgg(fig[i], master=contenedor)
        canvas_widget = canvas[i].get_tk_widget()
        canvas_widget.config(width=360, height=360)  # Tamaño fijo de 360x360 píxeles
        canvas_widget.grid(row=0, column=i, padx=5, pady=5)

    # Crear un marco para el botón de cerrar
    marco_boton = tk.Frame(nueva_ventana, bg='blue')
    marco_boton.pack(side='bottom', anchor='w', padx=20, pady=20)

    # Botón para cerrar la nueva ventana
    cerrar_boton = tk.Button(marco_boton, text="Cerrar", command=nueva_ventana.destroy)
    cerrar_boton.pack()

    # Ajustar la cuadrícula del contenedor para que mantenga el tamaño y posición de los gráficos
    contenedor.update_idletasks()
    ancho_contenedor = contenedor.winfo_width()
    contenedor.grid_columnconfigure(0, weight=1)
    contenedor.grid_columnconfigure(1, weight=1)
    contenedor.grid_columnconfigure(2, weight=1)

# Crear la ventana principal
root = tk.Tk()
root.title("PROYECTO CANSAT")

# Obtener tamaño de pantalla
pantalla_ancho = root.winfo_screenwidth()
pantalla_alto = root.winfo_screenheight()

# Ajustar tamaño de la ventana principal para que ocupe toda la pantalla
root.geometry(f"{pantalla_ancho}x{pantalla_alto}")

# Crear un Label para la imagen de fondo
try:
    fondo_imagen = PhotoImage(file=ruta_fondo_main)
    fondo_label = tk.Label(root, image=fondo_imagen)
    fondo_label.place(relwidth=1, relheight=1)
except Exception as e:
    print(f"Error al cargar la imagen de fondo: {e}")

# Crear un marco para contener la imagen y el selector
marco_contenedor = tk.Frame(root, bg='#04111d')
marco_contenedor.place(relx=0.5, rely=0.40, anchor='center')

# Cargar y mostrar la imagen
try:
    imagen = PhotoImage(file=ruta_imagen)
    label_imagen = tk.Label(marco_contenedor, image=imagen, bg='#153553')
    label_imagen.pack(pady=5)
except Exception as e:
    print(f"Error al cargar la imagen principal: {e}")

# Crear un marco para el texto, el selector y el botón OK
marco_selector = tk.Frame(marco_contenedor, bg='#153553')
marco_selector.pack(pady=0.02)

# Crear el widget Label para la instrucción
label = tk.Label(marco_selector, text="Seleccionar puerto COM", font=("Helvetica", 14), bg='#153553')
label.pack(pady=3)

# Crear y colocar el widget Combobox dentro del marco
combo_puertos = ttk.Combobox(marco_selector, state='readonly')
combo_puertos.pack(pady=2)

# Crear y colocar el botón "OK" dentro del marco (mantener siempre la misma distancia del Combobox)
boton_ok = tk.Button(marco_selector, text="Conectar", command=mostrar_nueva_interfaz, state=tk.NORMAL)
boton_ok.pack(pady=5)

# Crear y colocar el widget Label para mostrar el mensaje
mensaje = tk.Label(root, text="", bg='#153553')
mensaje.pack(pady=10)

# Ejecutar el bucle principal de la aplicación
root.mainloop()
