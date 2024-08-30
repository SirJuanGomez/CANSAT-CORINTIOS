import json
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def read_json_data(filename="sensor_data.json"):
    """Lee los datos de un archivo JSON."""
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        if not isinstance(data, list):
            print("El formato de datos es incorrecto, se esperaba una lista.")
            return None
        return data
    except FileNotFoundError:
        print(f"El archivo {filename} no se encontró.")
        return None
    except json.JSONDecodeError:
        print("Error al decodificar el archivo JSON.")
        return None

def plot_data(data):
    """Genera gráficos para cada variable."""
    if not isinstance(data, list) or not all(isinstance(d, dict) for d in data):
        print("Formato de datos incorrecto.")
        return None

    temperature = [d["temperature"] for d in data]
    pressure = [d["pressure"] for d in data]
    altitude = [d["altitude"] for d in data]

    fig, axs = plt.subplots(3, 1, figsize=(8, 6))
    axs[0].plot(temperature)
    axs[0].set_title("Temperatura")
    axs[1].plot(pressure)
    axs[1].set_title("Presión")
    axs[2].plot(altitude)
    axs[2].set_title("Altitud")

    plt.tight_layout()
    return fig

def update_plot():
    """Actualiza la gráfica con los datos del archivo JSON."""
    data = read_json_data()
    print("Datos leídos:", data)  # Añadido para depuración
    if data:
        fig = plot_data(data)
        if fig:
            # Borra el widget anterior si existe
            for widget in canvas_frame.winfo_children():
                widget.destroy()
            # Crea un nuevo widget de lienzo y lo coloca en el marco
            global canvas
            canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.grid(row=0, column=0, sticky="nsew")
            canvas.draw()
    # Programa la próxima actualización
    root.after(1000, update_plot)  # Actualizar cada 5000 milisegundos (5 segundos)

# Crear la ventana principal
root = tk.Tk()
root.title("Visualización de Datos")

# Crear un marco para contener la gráfica
canvas_frame = ttk.Frame(root)
canvas_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

# Botón para iniciar la actualización automática (opcional)
start_button = ttk.Button(root, text="Iniciar Actualización Automática", command=lambda: update_plot())
start_button.grid(row=0, column=0, padx=10, pady=10)

# Iniciar la actualización automática al iniciar
root.after(5000, update_plot)  # Actualizar cada 5000 milisegundos (5 segundos)

# Ajustar el tamaño del marco
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)

# Iniciar la aplicación
root.mainloop()