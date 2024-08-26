import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
import serial
import serial.tools.list_ports
import threading
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Listas de datos
tiempos = []
temperaturas = []
presiones = []
altitudes = []
start_time = time.time()
canvas = [None] * 3
ax = [None] * 3
fig = [None] * 3
fondo_imagen = None

def obtener_puertos_com():
    puertos = serial.tools.list_ports.comports()
    lista_puertos = [puerto.device for puerto in puertos]
    if not lista_puertos:
        lista_puertos = ["(Vacio)"]
    return lista_puertos

def actualizar_puertos():
    puertos_disponibles = obtener_puertos_com()
    combo_puertos['values'] = puertos_disponibles
    if combo_puertos.get() not in puertos_disponibles:
        combo_puertos.set("")
    root.after(500, actualizar_puertos)

def leer_datos_com(puerto_com, velocidad_baudios):
    try:
        with serial.Serial(puerto_com, velocidad_baudios, timeout=1) as ser:
            while True:
                if ser.in_waiting > 0:
                    datos = ser.readline().decode('utf-8').strip()
                    try:
                        temperatura, presion, altitud, timestamp = datos.split(',')
                        tiempo_actual = time.time() - start_time
                        temperaturas.append(float(temperatura))
                        presiones.append(float(presion))
                        altitudes.append(float(altitud))
                        tiempos.append(tiempo_actual)
                        if len(tiempos) > 100:
                            tiempos.pop(0)
                            temperaturas.pop(0)
                            presiones.pop(0)
                            altitudes.pop(0)
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
    mensaje.config(text=mensaje_texto)

def actualizar_graficas():
    global ax, canvas, fig
    for i in range(3):
        if ax[i] is not None and fig[i] is not None:
            ax[i].clear()
    if ax[0] is not None and fig[0] is not None:
        ax[0].plot(tiempos, temperaturas, label='Temperatura vs Tiempo', color='blue')
        ax[0].set_xlabel('Tiempo (s)')
        ax[0].set_ylabel('Temperatura (°C)')
        ax[0].legend()
    if ax[1] is not None and fig[1] is not None:
        ax[1].plot(tiempos, presiones, label='Presión vs Tiempo', color='green')
        ax[1].set_xlabel('Tiempo (s)')
        ax[1].set_ylabel('Presión (hPa)')
        ax[1].legend()
    if ax[2] is not None and fig[2] is not None:
        ax[2].plot(tiempos, altitudes, label='Altitud vs Tiempo', color='red')
        ax[2].set_xlabel('Tiempo (s)')
        ax[2].set_ylabel('Altitud (m)')
        ax[2].legend()
    
    for i in range(3):
        if canvas[i] is not None:
            canvas[i].draw()

def iniciar_lectura():
    puerto_seleccionado = combo_puertos.get()
    if puerto_seleccionado != "No se encontraron puertos COM" and puerto_seleccionado:
        hilo_lectura = threading.Thread(target=leer_datos_com, args=(puerto_seleccionado, 115200))
        hilo_lectura.daemon = True
        hilo_lectura.start()
        root.withdraw()
        mostrar_nueva_interfaz()
    else:
        actualizar_mensaje("Por favor, selecciona un puerto COM válido.")

def mostrar_nueva_interfaz():
    global canvas, ax, fig, fondo_imagen 
    nueva_ventana = tk.Toplevel(root)
    nueva_ventana.title("CANSAT CORINTIOS")
    pantalla_ancho = nueva_ventana.winfo_screenwidth()
    pantalla_alto = nueva_ventana.winfo_screenheight()
    nueva_ventana.geometry(f"{pantalla_ancho}x{pantalla_alto}+0+0")
    nueva_ventana.resizable(True, True)
    fondo_imagen = PhotoImage(file=r"c:\Users\SJG\Desktop\Proyecto Cansat\Fondo Main.png")
    fondo_label = tk.Label(nueva_ventana, image=fondo_imagen)
    fondo_label.place(relwidth=1, relheight=1)
    contenedor = tk.Frame(nueva_ventana, bg='#153553')
    contenedor.place(relx=0.5, rely=0.5, anchor='center')
    for i in range(3):
        fig[i], ax[i] = plt.subplots(figsize=(6, 6), dpi=100) 
        ax[i].set_title(["Temperatura vs Tiempo", "Presión vs Tiempo", "Altitud vs Tiempo"][i])
        canvas[i] = FigureCanvasTkAgg(fig[i], master=contenedor)
        canvas_widget = canvas[i].get_tk_widget()
        canvas_widget.config(width=360, height=260)
        canvas_widget.grid(row=0, column=i, padx=15, pady=5)
    marco_boton = tk.Frame(nueva_ventana, bg='#153553')
    marco_boton.pack(side='bottom', anchor='w', padx=20, pady=20)
    volver_boton = tk.Button(marco_boton, text="Volver", command=lambda: [nueva_ventana.destroy(), restaurar_ventana_principal()])
    volver_boton.pack(side='top_right', padx=10)
    cerrar_boton = tk.Button(marco_boton, text="Cerrar", command=nueva_ventana.destroy)
    cerrar_boton.pack(side='left', padx=10)
    contenedor.update_idletasks()
    contenedor.grid_columnconfigure(0, weight=1)
    contenedor.grid_columnconfigure(1, weight=1)
    contenedor.grid_columnconfigure(2, weight=1)

def restaurar_ventana_principal():
    global fondo_imagen
    root.deiconify() 
    fondo_label.config(image=fondo_imagen)

def actualizar_estado_boton():
    if combo_puertos.get() == "(Vacio)" or not combo_puertos.get():
        boton_ok.config(state=tk.DISABLED)
    else:
        boton_ok.config(state=tk.NORMAL)

root = tk.Tk()
root.title("PROYECTO CANSAT")

icono_imagen = tk.PhotoImage(file=r"c:\Users\SJG\Desktop\Proyecto Cansat\Imagenes\icono.png")
root.iconphoto(False, icono_imagen)

pantalla_ancho = root.winfo_screenwidth()
pantalla_alto = root.winfo_screenheight()
root.geometry(f"{pantalla_ancho}x{pantalla_alto}+0+0")
fondo_imagen = PhotoImage(file=r"c:\Users\SJG\Desktop\Proyecto Cansat\Imagenes\Fondo Main.png")
fondo_label = tk.Label(root, image=fondo_imagen)
fondo_label.place(relwidth=1, relheight=1)
fondo_imagen_frame = PhotoImage(file=r"c:\Users\SJG\Desktop\Proyecto Cansat\Imagenes\Fondo Main.png")
marco_contenedor = tk.Frame(root, bg='#04111d')
marco_contenedor.place(relx=0.5, rely=0.40, anchor='center')
fondo_label_frame = tk.Label(marco_contenedor, image=fondo_imagen_frame, bg='white')
fondo_label_frame.place(relwidth=1, relheight=1)
imagen = tk.PhotoImage(file=r"c:\Users\SJG\Desktop\Proyecto Cansat\Imagenes\Main.png")
label_imagen = tk.Label(marco_contenedor, image=imagen, bg='#153553')
label_imagen.pack(pady=5)
marco_selector = tk.Frame(marco_contenedor, bg='#153553')
marco_selector.pack(pady=0.02)
label = tk.Label(marco_selector, text="Seleccionar puerto COM", font=("Capture it", 16), bg='#153553')
label.pack(pady=3)
combo_puertos = ttk.Combobox(marco_selector, state='readonly')
combo_puertos.pack(pady=2)
boton_ok = tk.Button(marco_selector, text="Conectar", command=iniciar_lectura, state=tk.DISABLED)
boton_ok.pack(pady=5)
mensaje = tk.Label(root, text="", bg='#153553')
mensaje.pack(pady=10)
combo_puertos.bind("<<ComboboxSelected>>", lambda event: actualizar_estado_boton())
actualizar_puertos()
root.mainloop()