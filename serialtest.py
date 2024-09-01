import serial
import json
import os
from datetime import datetime
import time

# Nombre del archivo de estado
status_file = 'status.txt'

# Nombre del archivo JSON
json_filename = 'sensor_data.json'

# Número máximo de entradas en el archivo JSON
MAX_ENTRIES = 20

def read_status():
    """Lee el valor del archivo de estado y devuelve el valor entero."""
    if os.path.exists(status_file):
        with open(status_file, 'r') as f:
            try:
                return int(f.read().strip())
            except ValueError:
                return 0
    return 0

def load_data():
    """Carga datos existentes del archivo JSON."""
    if os.path.exists(json_filename):
        with open(json_filename, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def save_data(data_list):
    """Guarda datos en el archivo JSON."""
    with open(json_filename, 'w') as file:
        json.dump(data_list, file, indent=4)

def main():
    # Configura el puerto serial
    ser = serial.Serial('COM4', 115200, timeout=1)  # Cambia 'COM4' al puerto serial correcto
    
    # Inicializar la lista de datos
    data_list = load_data()
    
    while True:
        if read_status() == 1:
            try:
                # Leer una línea de datos desde el puerto serial
                line = ser.readline().decode('utf-8').strip()
                
                if line:
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
        else:
            print("El estado no es 1. El proceso se detendrá.")
            break

    # Cierra el puerto serial cuando termines
    ser.close()

if __name__ == "__main__":
    main()
