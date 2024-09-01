import tkinter as tk
from tkinter import PhotoImage, scrolledtext
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import serial
import threading
import time

# Variables globales
temperaturas = []
presiones = []
altitudes = []
tiempos = []
start_time = time.time()
canvas = [None, None, None]
ax = [None, None, None]
fig = [None, None, None]
valor_uv_label = None
valor_gx_label = None
valor_gy_label = None
valor_gz_label = None
texto_serial = None

# Ruta de la imagen de fondo
ruta_fondo_main = "Imagenes/FondoMain.png"

def actualizar_mensaje(mensaje):
    """Actualiza la etiqueta de mensaje en la interfaz."""
    mensaje_label.config(text=mensaje)

def actualizar_graficas():
    """Actualiza las gráficas en la interfaz."""
    for i, ax_i in enumerate(ax):
        ax_i.clear()
        if i == 0:
            ax_i.plot(tiempos, temperaturas, label="Temperatura (°C)", color='r')
        elif i == 1:
            ax_i.plot(tiempos, presiones, label="Presión (hPa)", color='b')
        elif i == 2:
            ax_i.plot(tiempos, altitudes, label="Altitud (m)", color='g')
        ax_i.legend()
        ax_i.set_xlabel("Tiempo (s)")
        ax_i.set_ylabel(["Temperatura (°C)", "Presión (hPa)", "Altitud (m)"][i])
        ax_i.set_title(["Temperatura vs Tiempo", "Presión vs Tiempo", "Altitud vs Tiempo"][i])
        canvas[i].draw()

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

    # Crear un marco para mostrar los valores UV y giroscopio
    marco_datos = tk.Frame(nueva_ventana, bg='lightgray')
    marco_datos.pack(side='right', padx=10, pady=10, fill='y')

    # Labels para mostrar los valores de UV y giroscopio
    global valor_uv_label, valor_gx_label, valor_gy_label, valor_gz_label
    tk.Label(marco_datos, text="UV Sensor Value:", font=("Helvetica", 12), bg='lightgray').pack(pady=5)
    valor_uv_label = tk.Label(marco_datos, text="0", font=("Helvetica", 12), bg='white')
    valor_uv_label.pack(pady=5)

    tk.Label(marco_datos, text="Gyroscope Values:", font=("Helvetica", 12), bg='lightgray').pack(pady=5)
    valor_gx_label = tk.Label(marco_datos, text="Gx: 0", font=("Helvetica", 12), bg='white')
    valor_gx_label.pack(pady=5)
    valor_gy_label = tk.Label(marco_datos, text="Gy: 0", font=("Helvetica", 12), bg='white')
    valor_gy_label.pack(pady=5)
    valor_gz_label = tk.Label(marco_datos, text="Gz: 0", font=("Helvetica", 12), bg='white')
    valor_gz_label.pack(pady=5)

    # Crear un marco para el área de texto de los datos del puerto COM
    marco_texto = tk.Frame(nueva_ventana)
    marco_texto.pack(side='left', padx=10, pady=10, fill='both', expand=True)

    # Área de texto para visualizar los datos del puerto COM
    global texto_serial
    texto_serial = scrolledtext.ScrolledText(marco_texto, width=60, height=20, wrap=tk.WORD)
    texto_serial.pack(padx=5, pady=5, fill='both', expand=True)

    # Crear un marco para el botón de cerrar
    marco_boton = tk.Frame(nueva_ventana, bg='blue')
    marco_boton.pack(side='bottom', anchor='w', padx=20, pady=20)

    # Botón para cerrar la nueva ventana
    tk.Button(marco_boton, text="Cerrar", command=nueva_ventana.destroy).pack()

    # Ajustar la cuadrícula del contenedor para que mantenga el tamaño y posición de los gráficos
    contenedor.update_idletasks()
    contenedor.grid_columnconfigure(0, weight=1)
    contenedor.grid_columnconfigure(1, weight=1)
    contenedor.grid_columnconfigure(2, weight=1)

def leer_datos_com(puerto_com, velocidad_baudios):
    """Lee datos del puerto COM en un hilo separado."""
    global hilo_lectura
    try:
        with serial.Serial(puerto_com, velocidad_baudios, timeout=1) as ser:  # "timeout=1" reset cada 1 segundo
            while True:
                if ser.in_waiting > 0:
                    datos = ser.readline().decode('utf-8').strip()
                    try:
                        temperatura, presion, altitud, gx, gy, gz, uvValue, uvVoltage, timestamp = datos.split(',')
                        tiempo_actual = time.time() - start_time
                        temperaturas.append(float(temperatura))
                        presiones.append(float(presion))
                        altitudes.append(float(altitud))
                        tiempos.append(tiempo_actual)

                        # Actualiza las labels con los nuevos valores
                        root.after(0, lambda: valor_uv_label.config(text=f"{uvValue} V ({uvVoltage} V)"))
                        root.after(0, lambda: valor_gx_label.config(text=f"Gx: {gx}"))
                        root.after(0, lambda: valor_gy_label.config(text=f"Gy: {gy}"))
                        root.after(0, lambda: valor_gz_label.config(text=f"Gz: {gz}"))

                        # Limita el tamaño de las listas para evitar sobrecargar la memoria
                        if len(tiempos) > 100:
                            tiempos.pop(0)
                            temperaturas.pop(0)
                            presiones.pop(0)
                            altitudes.pop(0)

                        # Actualiza las gráficas
                        root.after(0, actualizar_graficas)

                        # Muestra los datos en el área de texto
                        texto_serial.insert(tk.END, f"{datos}\n")
                        texto_serial.yview(tk.END)  # Desplaza hacia abajo para mostrar el nuevo texto

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

def iniciar_lectura_datos():
    """Inicia el hilo para leer datos del puerto COM."""
    puerto_com = entrada_puerto_com.get()
    velocidad_baudios = int(entrada_baudios.get())
    hilo_lectura = threading.Thread(target=leer_datos_com, args=(puerto_com, velocidad_baudios), daemon=True)
    hilo_lectura.start()
    mostrar_nueva_interfaz()

# Configuración inicial de la interfaz
root = tk.Tk()
root.title("Interfaz CANSAT")

# Crear el marco para las entradas y botones
marco_entrada = tk.Frame(root)
marco_entrada.pack(padx=10, pady=10)

# Crear etiquetas y entradas para el puerto COM y la velocidad de baudios
tk.Label(marco_entrada, text="Puerto COM:").grid(row=0, column=0, padx=5, pady=5)
entrada_puerto_com = tk.Entry(marco_entrada)
entrada_puerto_com.grid(row=0, column=1, padx=5, pady=5)

tk.Label(marco_entrada, text="Velocidad de Baudios:").grid(row=1, column=0, padx=5, pady=5)
entrada_baudios = tk.Entry(marco_entrada)
entrada_baudios.grid(row=1, column=1, padx=5, pady=5)

# Crear un botón para iniciar la lectura de datos
tk.Button(marco_entrada, text="Iniciar", command=iniciar_lectura_datos).grid(row=2, columnspan=2, pady=10)

# Crear una etiqueta para mostrar mensajes de estado
mensaje_label = tk.Label(root, text="")
mensaje_label.pack(pady=10)

root.mainloop()
