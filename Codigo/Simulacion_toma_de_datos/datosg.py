import json
import time
import random
import os

def generate_data():
    """Genera datos de temperatura, presión, altitud, giroscopio, aceleración y UV."""
    temperature = round(random.uniform(10, 30), 2)
    pressure = round(random.uniform(980, 1030), 2)
    altitude = round(random.uniform(0, 1000), 2)
    
    # Generar datos para el giroscopio (en ejes X, Y, Z)
    gx = round(random.uniform(-500, 500), 2)
    gy = round(random.uniform(-500, 500), 2)
    gz = round(random.uniform(-500, 500), 2)
    
    # Generar datos para la aceleración (en ejes X, Y, Z)
    ax = round(random.uniform(-10, 10), 2)
    ay = round(random.uniform(-10, 10), 2)
    az = round(random.uniform(-10, 10), 2)
    
    # Generar datos para el sensor UV
    uvVoltage = round(random.uniform(0, 5), 2)
    
    return {
        "temperature": temperature,
        "pressure": pressure,
        "altitude": altitude,
        "gx": gx,
        "gy": gy,
        "gz": gz,
        "ax": ax,
        "ay": ay,
        "az": az,
        "uvVoltage": uvVoltage,
    }

def load_existing_data(filename="sensor_data.json"):
    """Carga los datos existentes del archivo JSON."""
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            try:
                data = json.load(f)
                if not isinstance(data, list):
                    print("Formato de datos incorrecto en el archivo. Se creará un nuevo archivo.")
                    return []
                return data
            except json.JSONDecodeError:
                print("Error al decodificar el archivo JSON.")
                return []
    return []

def save_data_to_file(data, filename="sensor_data.json"):
    """Guarda los datos en un archivo JSON."""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def trim_data(data, max_size=100):
    """Mantiene solo los últimos `max_size` datos."""
    return data[-max_size:]

def should_run(status_folder="estados", status_filename="estados.json"):
    """Verifica si el script debe ejecutarse basado en el archivo de estado."""
    status_file_path = os.path.join(status_folder, status_filename)
    if os.path.exists(status_file_path):
        with open(status_file_path, 'r') as f:
            try:
                status_data = json.load(f)
                # Se asume que status_data es una lista y se toma el primer elemento
                status = status_data[0].get("run", 0)
                return status == 1
            except (json.JSONDecodeError, IndexError):
                print("Error al leer el archivo de estado JSON o el formato del archivo es incorrecto.")
                return False
    else:
        print("El archivo de estado no existe. No se ejecutará el script.")
        return False

if __name__ == "__main__":
    filename = "sensor_data.json"
    status_folder = "estados"
    status_filename = "estados.json"
    max_data_points = 10  # Número máximo de puntos de datos a mantener

    print("Verificando estado inicial...")
    if should_run(status_folder, status_filename):
        print("El estado 'run' es 1. Comenzando la generación de datos.")
        while True:
            if not should_run(status_folder, status_filename):
                print("El estado 'run' ha cambiado a 0. Deteniendo la generación de datos.")
                break

            new_data = generate_data()
            print(f"Datos en tiempo real: {new_data}")

            # Cargar datos existentes
            data_list = load_existing_data(filename)
            # Añadir los nuevos datos
            data_list.append(new_data)
            # Mantener solo los datos más recientes
            data_list = trim_data(data_list, max_size=max_data_points)
            # Guardar los datos actualizados en el archivo
            save_data_to_file(data_list, filename)

            time.sleep(1)  # Espera 1 segundo antes de generar nuevos datos
    else:
        print("El estado 'run' no es 1. El script no está en ejecución.")
