import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
import serial
import serial.tools.list_ports
import threading
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Variables globales para almacenar datos
tiempos = []
temperaturas = []
presiones = []
altitudes = []
start_time = time.time()  # Definir start_time globalmente
canvas = [None] * 3
ax = [None] * 3
fig = [None] * 3

def obtener_puertos_com():
    """Obtiene una lista de puertos COM disponibles."""
    puertos = serial.tools.list_ports.comports()
    lista_puertos = [puerto.device for puerto in puertos]
    if not lista_puertos:
        lista_puertos = ["No se encontraron puertos COM"]
    return lista_puertos

def actualizar_puertos():
    """Actualiza la lista de puertos COM en el Combobox."""
    puertos_disponibles = obtener_puertos_com()
    combo_puertos['values'] = puertos_disponibles
    if combo_puertos.get() not in puertos_disponibles:
        combo_puertos.set("")

    # Volver a ejecutar la función después de 500 ms 
    root.after(500, actualizar_puertos)

def leer_datos_com(puerto_com, velocidad_baudios):
    """Lee datos del puerto COM en un hilo separado."""
    try:
        with serial.Serial(puerto_com, velocidad_baudios, timeout=1) as ser:
            while True:
                if ser.in_waiting > 0:
                    datos = ser.readline().decode('utf-8').strip()
                    # Suponiendo que los datos vienen en el formato "temperatura,presion,altitud,timestamp"
                    try:
                        temperatura, presion, altitud, timestamp = datos.split(',')
                        tiempo_actual = time.time() - start_time
                        temperaturas.append(float(temperatura))
                        presiones.append(float(presion))
                        altitudes.append(float(altitud))
                        tiempos.append(tiempo_actual)
                        # Limita el tamaño de las listas para evitar sobrecargar la memoria
                        if len(tiempos) > 100:
                            tiempos.pop(0)
                            temperaturas.pop(0)
                            presiones.pop(0)
                            altitudes.pop(0)
                        # Actualiza las gráficas
                        root.after(0, actualizar_graficas)
                    except ValueError:
                        root.after(0, actualizar_mensaje, "Error: Datos no válidos recibidos.")
                time.sleep(0.1)
    except serial.SerialException as e:
        if "Access is denied" in str(e):
            root.after(0, actualizar_mensaje, "Error: Acceso denegado. Verifica que el puerto COM no esté en uso.")
        else:
            root.after(0, actualizar_mensaje, f"Error en la conexión serial: {e}")
    except Exception as e:
        root.after(0, actualizar_mensaje, f"Error inesperado: {e}")

def actualizar_mensaje(mensaje_texto):
    """Actualiza el mensaje en la interfaz gráfica."""
    mensaje.config(text=mensaje_texto)

def actualizar_graficas():
    """Actualiza todas las gráficas en tiempo real."""
    global ax, canvas, fig
    for i in range(3):
        if ax[i] is not None and fig[i] is not None:
            ax[i].clear()
    # Actualiza la gráfica de temperatura
    if ax[0] is not None and fig[0] is not None:
        ax[0].plot(tiempos, temperaturas, label='Temperatura vs Tiempo', color='blue')
        ax[0].set_xlabel('Tiempo (s)')
        ax[0].set_ylabel('Temperatura (°C)')
        ax[0].legend()

    # Actualiza la gráfica de presión atmosférica
    if ax[1] is not None and fig[1] is not None:
        ax[1].plot(tiempos, presiones, label='Presión vs Tiempo', color='green')
        ax[1].set_xlabel('Tiempo (s)')
        ax[1].set_ylabel('Presión (hPa)')
        ax[1].legend()

    # Actualiza la gráfica de altitud
    if ax[2] is not None and fig[2] is not None:
        ax[2].plot(tiempos, altitudes, label='Altitud vs Tiempo', color='red')
        ax[2].set_xlabel('Tiempo (s)')
        ax[2].set_ylabel('Altitud (m)')
        ax[2].legend()
    
    for i in range(3):
        if canvas[i] is not None:
            canvas[i].draw()

def iniciar_lectura():
    """Inicia el proceso de lectura de datos y cambia a una nueva interfaz."""
    puerto_seleccionado = combo_puertos.get()
    if puerto_seleccionado != "No se encontraron puertos COM" and puerto_seleccionado:
        # Inicia un nuevo hilo para leer datos del puerto COM
        hilo_lectura = threading.Thread(target=leer_datos_com, args=(puerto_seleccionado, 115200))
        hilo_lectura.daemon = True  # Termina el hilo cuando se cierra la ventana
        hilo_lectura.start()
        # Oculta la ventana actual y muestra la nueva interfaz
        root.withdraw()
        mostrar_nueva_interfaz()
    else:
        actualizar_mensaje("Por favor, selecciona un puerto COM válido.")

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
    fondo_imagen = PhotoImage(file=r"c:\Users\SJG\Desktop\Proyecto Cansat\FondoMainGraficas.png")  # Cambia esto por la ruta de tu imagen
    fondo_label = tk.Label(nueva_ventana, image=fondo_imagen)
    fondo_label.place(relwidth=1, relheight=1)

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
    #marco_boton = tk.Frame(nueva_ventana, bg='blue')
    #marco_boton.pack(side='bottom', anchor='w', padx=20, pady=20)

    # Botón para cerrar la nueva ventana
    #cerrar_boton = tk.Button(marco_boton, text="Cerrar", command=nueva_ventana.destroy)
    #cerrar_boton.pack()

    # Ajustar la cuadrícula del contenedor para que mantenga el tamaño y posición de los gráficos
    contenedor.update_idletasks()
    ancho_contenedor = contenedor.winfo_width()
    contenedor.grid_columnconfigure(0, weight=1)
    contenedor.grid_columnconfigure(1, weight=1)
    contenedor.grid_columnconfigure(2, weight=1)

def actualizar_estado_boton():
    """Actualiza el estado del botón 'OK' según la selección del puerto COM."""
    if combo_puertos.get() == "No se encontraron puertos COM" or not combo_puertos.get():
        boton_ok.config(state=tk.DISABLED)
    else:
        boton_ok.config(state=tk.NORMAL)

# Crear la ventana principal
root = tk.Tk()
root.title("PROYECTO CANSAT")

# Obtener tamaño de pantalla
pantalla_ancho = root.winfo_screenwidth()
pantalla_alto = root.winfo_screenheight()

# Ajustar tamaño de la ventana principal para que ocupe toda la pantalla
root.geometry(f"{pantalla_ancho}x{pantalla_alto}")

# Crear un Label para la imagen de fondo
fondo_imagen = PhotoImage(file=r"c:\Users\SJG\Desktop\Proyecto Cansat\Fondo Main.png")  # Cambia esto por la ruta de tu imagen
fondo_label = tk.Label(root, image=fondo_imagen)
fondo_label.place(relwidth=1, relheight=1)

# Crear un Label para la imagen de fondo del marco de selección
fondo_imagen_frame = PhotoImage(file=r"c:\Users\SJG\Desktop\Proyecto Cansat\Fondo Main.png")  # Cambia esto por la ruta de tu imagen

# Crear un marco para contener la imagen y el selector
marco_contenedor = tk.Frame(root, bg='#04111d')
marco_contenedor.place(relx=0.5, rely=0.40, anchor='center')

# Colocar el Label de imagen de fondo en el marco del contenedor
fondo_label_frame = tk.Label(marco_contenedor, image=fondo_imagen_frame, bg='white')
fondo_label_frame.place(relwidth=1, relheight=1)

# Cargar y mostrar la imagen
imagen = tk.PhotoImage(file=r"c:\Users\SJG\Desktop\Proyecto Cansat\Main.png")  # Cambia esto por la ruta de tu imagen
label_imagen = tk.Label(marco_contenedor, image=imagen, bg='#153553')
label_imagen.pack(pady=5)

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
boton_ok = tk.Button(marco_selector, text="Conectar", command=iniciar_lectura, state=tk.DISABLED)
boton_ok.pack(pady=5)

# Crear y colocar el widget Label para mostrar el mensaje
mensaje = tk.Label(root, text="", bg='#153553')
mensaje.pack(pady=10)

# Actualizar el estado del botón "OK" al cambiar la selección del Combobox
combo_puertos.bind("<<ComboboxSelected>>", lambda event: actualizar_estado_boton())

# Iniciar la actualización periódica de puertos COM
actualizar_puertos()

# Ejecutar el bucle principal de la aplicación
root.mainloop()