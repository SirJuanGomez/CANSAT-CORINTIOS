import serial
import json
import os
import sys
from datetime import datetime

# Obtener argumentos de línea de comandos
if len(sys.argv) != 3:
    print("Uso: python serialtest2.py <puerto_com> <baud_rate>")
    sys.exit(1)

com_port = sys.argv[1]
baud_rate = int(sys.argv[2])

# Nombre del archivo JSON
json_filename = 'sensor_data.json'

# Número máximo de entradas en el archivo JSON
MAX_ENTRIES = 20

# Cargar datos existentes del archivo JSON
def load_data():
    if os.path.exists(json_filename):
        with open(json_filename, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

# Guardar datos en el archivo JSON
def save_data(data_list):
    with open(json_filename, 'w') as file:
        json.dump(data_list, file, indent=4)

# Inicializar la lista de datos
data_list = load_data()

try:
    # Configura el puerto serial
    ser = serial.Serial(com_port, baud_rate, timeout=1)
except serial.SerialException as e:
    print(f"Error al abrir el puerto COM: {e}")
    sys.exit(1)

while True:
    try:
        # Leer una línea de datos desde el puerto serial
        line = ser.readline().decode('utf-8').strip()
        
        if line:
            # Los datos ya están en formato JSON, simplemente los cargamos
            try:
                data = json.loads(line)
                print("Datos recibidos:")
                print(data)
                
                # Agregar los datos a la lista
                data_list.append(data)
                
                # Comprobar si la lista alcanza el máximo de entradas
                if len(data_list) > MAX_ENTRIES:
                    # Mantener solo las últimas MAX_ENTRIES entradas
                    data_list = data_list[-MAX_ENTRIES:]
                
                # Guardar la lista actualizada en el archivo JSON
                save_data(data_list)
                    
            except json.JSONDecodeError:
                print("Error al decodificar JSON:", line)

    except KeyboardInterrupt:
        # Guardar los datos restantes al finalizar
        if data_list:
            save_data(data_list)
        print("Programa interrumpido por el usuario.")
        break
    except Exception as e:
        print("Error:", e)

# Cierra el puerto serial cuando termines
ser.close()
