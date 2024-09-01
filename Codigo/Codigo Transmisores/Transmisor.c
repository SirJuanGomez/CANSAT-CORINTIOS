#include <Wire.h>
#include <Adafruit_BMP280.h>
#include <MPU6050.h>
#include <RF24.h>

// Definir pines del nRF24L01
#define CE_PIN   4
#define CSN_PIN  5

// Crear instancia del objeto RF24
RF24 radio(CE_PIN, CSN_PIN);

// Crear instancias para los sensores
Adafruit_BMP280 bmp;  // Para el BMP280
MPU6050 mpu;          // Para el MPU6050

// Dirección del canal de comunicación (debe ser la misma en el receptor)
const byte address[6] = "00001";

// Definir el pin analógico para el GY-ML8511
#define UV_SENSOR_PIN 34

// Variable global para almacenar el timestamp
unsigned long timestamp = 0;

void setup() {
  // Inicializar comunicación serial
  Serial.begin(115200);

  // Inicializar el bus I2C
  Wire.begin();

  // Inicializar el BMP280
  if (!bmp.begin(0x76)) {
    Serial.println(F("No se encontró un BMP280 válido, verifique las conexiones!"));
    while (1);
  }

  // Inicializar el MPU6050
  mpu.initialize();
  
  if (!mpu.testConnection()) {
    Serial.println("Error de conexión con el MPU6050.");
    while (1);
  }

  // Inicializar el módulo nRF24L01
  radio.begin();
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_HIGH); // Configura la potencia de transmisión
  radio.setDataRate(RF24_1MBPS); // Configura la velocidad de transmisión

  Serial.println("Sensores y nRF24L01 inicializados correctamente.");
}

void loop() {
  // Incrementar el timestamp
  timestamp++;

  // Leer datos del BMP280
  float temperature = bmp.readTemperature();
  float pressure = bmp.readPressure() / 100.0F;
  float altitude = bmp.readAltitude(1013.25);  // Leer la altitud basada en la presión

  // Leer datos del MPU6050
  int16_t ax, ay, az;
  int16_t gx, gy, gz;
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

  // Leer datos del GY-ML8511
  int uvSensorValue = analogRead(UV_SENSOR_PIN);
  float uvVoltage = (uvSensorValue / 4095.0) * 3.3; // Convertir valor ADC a voltaje

  // Crear un objeto JSON
  String jsonData = "{";
  jsonData += "\"timestamp\": " + String(timestamp) + ", ";
  jsonData += "\"temperature\": " + String(temperature, 2) + ", ";
  jsonData += "\"pressure\": " + String(pressure, 2) + ", ";
  jsonData += "\"altitude\": " + String(altitude, 2) + ", ";
  jsonData += "\"ax\": " + String(ax) + ", ";
  jsonData += "\"ay\": " + String(ay) + ", ";
  jsonData += "\"az\": " + String(az) + ", ";
  jsonData += "\"gx\": " + String(gx) + ", ";
  jsonData += "\"gy\": " + String(gy) + ", ";
  jsonData += "\"gz\": " + String(gz) + ", ";
  jsonData += "\"uvValue\": " + String(uvSensorValue) + ", ";
  jsonData += "\"uvVoltage\": " + String(uvVoltage, 2);
  jsonData += "}";

  // Enviar el JSON a través del módulo nRF24L01
  radio.write(jsonData.c_str(), jsonData.length());

  // Imprimir datos en el monitor serial
  Serial.println(jsonData);

  // Esperar 1 segundo antes de la siguiente lectura
  delay(1000);
}
