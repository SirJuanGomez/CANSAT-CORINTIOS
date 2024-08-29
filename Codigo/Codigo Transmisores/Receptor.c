#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

// Define los pines para CE y CSN en el Arduino
#define CE_PIN 9
#define CSN_PIN 10

RF24 radio(CE_PIN, CSN_PIN);  // Crea un objeto RF24
const byte direccion[6] = "00001";  // Dirección de la tubería de comunicación (debe coincidir con la del transmisor)

// Define una estructura que coincida con la enviada desde el transmisor
struct Mensaje {
  float temperatura;
  float presion;
  float altitud;
  float uvPromedio;
};

void setup() {
  // Inicializa la comunicación serial a 115200 baudios
  Serial.begin(115200);

  // Inicializa el módulo RF24
  if (!radio.begin()) {
    Serial.println("Error al inicializar el módulo NRF24L01.");
    while (1);
  }

  // Configura el canal de comunicación (debe coincidir con el canal del transmisor)
  radio.setChannel(108);

  // Configura la dirección de la tubería de comunicación
  radio.openReadingPipe(1, direccion);

  // Configura el nivel de potencia
  radio.setPALevel(RF24_PA_HIGH);

  // Configura el formato de datos
  radio.setDataRate(RF24_1MBPS);

  // Configura el modo de recepción
  radio.startListening();

  Serial.println("Modulo NRF24L01 configurado para recibir mensajes.");
}

void loop() {
  // Verifica si hay datos disponibles para leer
  if (radio.available()) {
    Mensaje recibido;

    // Lee los datos recibidos en la estructura
    radio.read(&recibido, sizeof(recibido));

    // Imprime los datos recibidos en el monitor serial
    Serial.print("Temperatura recibida: ");
    Serial.print(recibido.temperatura);
    Serial.println(" °C");

    Serial.print("Presión recibida: ");
    Serial.print(recibido.presion);
    Serial.println(" hPa");

    Serial.print("Altitud recibida: ");
    Serial.print(recibido.altitud);
    Serial.println(" m");

    Serial.print("UV Promedio recibido: ");
    Serial.print(recibido.uvPromedio);
    Serial.println(" V");
  } else {
    // Mensaje cuando no hay datos disponibles
    Serial.println("Esperando mensaje...");
    delay(1000);  // Espera 1 segundo antes de volver a verificar
  }
}
