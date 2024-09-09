import serial
import json
import os

# Especifica la ruta del archivo JSON
estados_file = 'Estados/estados.json'  # Cambia 'Estados' al nombre correcto del directorio
json_filename = 'sensor_data.json'

def check_serial_status():
    """Verifica el valor de 'serial' en el archivo JSON de estados."""
    if os.path.exists(estados_file):
        with open(estados_file, 'r') as file:
            try:
                data = json.load(file)
                # Asumimos que data es una lista con al menos un diccionario
                if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
                    return data[0].get('serial', 0) == 1
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Error al leer el archivo JSON de estados: {e}")
    return False

def save_data(data):
    """Guarda datos en el archivo JSON, reemplazando cualquier contenido existente."""
    with open(json_filename, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    if check_serial_status():
        try:
            # Configura el puerto serial
            ser = serial.Serial('COM4', 115200, timeout=1)  # Cambia 'COM4' al puerto serial correcto
        except serial.SerialException as e:
            print(f"Error al abrir el puerto serial: {e}")
            return  # Termina el programa si no se puede abrir el puerto
        
        while True:
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

        # Cierra el puerto serial cuando termines
        ser.close()
    else:
        print("El valor de 'serial' en el archivo JSON no es 1. El proceso se detendrá.")

if __name__ == "__main__":
    main()
