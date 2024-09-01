#include <Wire.h>
#include <Adafruit_BMP280.h>
#include <MPU6050.h>
#include <RF24.h>

// Definir pines del nRF24L01
#define CE_PIN   4
#define CSN_PIN  5

// Crear instancia del objeto RF24
RF24 radio(CE_PIN, CSN_PIN);

// Dirección del canal de comunicación (debe ser la misma en el emisor)
const byte address[6] = "00001";

void setup() {
  // Inicializar comunicación serial
  Serial.begin(115200);

  // Inicializar el módulo nRF24L01
  radio.begin();
  radio.openReadingPipe(1, address);
  radio.setPALevel(RF24_PA_HIGH);
  radio.setDataRate(RF24_1MBPS);
  radio.startListening();

  Serial.println("Receptor nRF24L01 inicializado correctamente.");
}

void loop() {
  if (radio.available()) {
    // Leer datos del nRF24L01
    char jsonData[256];  // Tamaño del buffer, ajustar según el tamaño de los datos
    radio.read(jsonData, sizeof(jsonData));

    // Enviar datos al puerto serial
    Serial.println(jsonData);
  }
}
