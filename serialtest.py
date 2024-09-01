import serial
import json
import os

# Nombre del archivo de estado
status_file = 'status.txt'

# Nombre del archivo JSON
json_filename = 'sensor_data.json'

def read_status():
    """Lee el valor del archivo de estado y devuelve el valor entero."""
    if os.path.exists(status_file):
        with open(status_file, 'r') as f:
            try:
                return int(f.read().strip())
            except ValueError:
                return 0
    return 0

def save_data(data):
    """Guarda datos en el archivo JSON, reemplazando cualquier contenido existente."""
    with open(json_filename, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    # Configura el puerto serial
    ser = serial.Serial('COM4', 115200, timeout=1)  # Cambia 'COM4' al puerto serial correcto
    
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
                        
                        # Guardar solo los datos nuevos, reemplazando los existentes en el archivo JSON
                        save_data([data])
                        
                    except json.JSONDecodeError:
                        print("Error al decodificar JSON:", line)
                
            except KeyboardInterrupt:
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
