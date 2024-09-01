import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
from collections import deque

# Nombre del archivo JSON
json_filename = 'sensor_data.json'

# Configuración de la gráfica
fig, axs = plt.subplots(2, 1, figsize=(12, 10))
ax1 = axs[0]
ax2 = axs[1]

# Configuración de las listas de datos
max_len = 100  # Número máximo de puntos en la gráfica
temperature_data = deque(maxlen=max_len)
pressure_data = deque(maxlen=max_len)
timestamps = deque(maxlen=max_len)

# Configuración de la gráfica de temperatura
line_temp, = ax1.plot([], [], marker='o', linestyle='-', color='b', label='Temperatura (°C)')
ax1.set_xlabel('Tiempo (s)')
ax1.set_ylabel('Temperatura (°C)')
ax1.set_title('Temperatura en Tiempo Real')
ax1.grid(True)
ax1.legend()

# Configuración de la gráfica de presión
line_pres, = ax2.plot([], [], marker='o', linestyle='-', color='r', label='Presión (hPa)')
ax2.set_xlabel('Tiempo (s)')
ax2.set_ylabel('Presión (hPa)')
ax2.set_title('Presión en Tiempo Real')
ax2.grid(True)
ax2.legend()

# Datos actuales del giroscopio y UV
text_box = ax2.text(0.1, 0.9, '', transform=ax2.transAxes, fontsize=12, verticalalignment='top')
ax2.axis('off')  # Desactiva los ejes para que solo se muestre el texto

# Leer los datos del archivo JSON
def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            try:
                data = json.load(file)
                # Si los datos no están en una lista, los convertimos en una lista
                if isinstance(data, dict):
                    return [data]
                return data
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Error al leer el archivo JSON: {e}")
                return []
    return []

# Función de inicialización para el gráfico
def init():
    line_temp.set_data([], [])
    line_pres.set_data([], [])
    text_box.set_text('')
    return line_temp, line_pres, text_box

# Función de actualización para la animación
def update(frame):
    data_list = load_data(json_filename)

    if not data_list:
        return line_temp, line_pres, text_box

    # Extraer timestamps, temperaturas y presiones
    global timestamps, temperature_data, pressure_data

    timestamps.append(data_list[-1]['timestamp'])
    temperature_data.append(data_list[-1]['temperature'])
    pressure_data.append(data_list[-1]['pressure'])
    
    # Datos actuales del giroscopio y UV
    latest_data = data_list[-1]
    gx = latest_data['gx']
    gy = latest_data['gy']
    gz = latest_data['gz']
    uv_voltage = latest_data['uvVoltage']

    # Actualizar gráficos
    line_temp.set_data(timestamps, temperature_data)
    line_pres.set_data(timestamps, pressure_data)
    
    # Ajustar los límites de los ejes
    ax1.set_xlim(min(timestamps), max(timestamps))
    ax1.set_ylim(0, 150)  # Ajustar el límite superior para la temperatura

    ax2.set_xlim(min(timestamps), max(timestamps))
    ax2.set_ylim(min(pressure_data) - 10, max(pressure_data) + 10)
    
    # Actualizar recuadro de valores
    text_box.set_text(
        f'Giroscopio X: {gx}\n'
        f'Giroscopio Y: {gy}\n'
        f'Giroscopio Z: {gz}\n'
        f'Voltaje UV: {uv_voltage:.2f} V'
    )
    
    return line_temp, line_pres, text_box

# Crear la animación
ani = animation.FuncAnimation(fig, update, init_func=init, blit=True, interval=1000)  # Intervalo en milisegundos

plt.tight_layout()
plt.show()
