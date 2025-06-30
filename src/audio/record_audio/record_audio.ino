#include <PDM.h>

static const char channels = 1;
static const int frequency = 16000; // 16 KHz

short sampleBuffer[1024];
volatile int samplesRead;

void setup() {
  Serial.begin(9600);
  while (!Serial);  // esperar conexion Serial

  PDM.onReceive(onPDMdata);
  PDM.setGain(30); // la ganancia

  if (!PDM.begin(channels, frequency)) {
    Serial.println("Failed to start PDM!");
    while (1);
  }
}

void loop() {
  if (samplesRead) {
    for (int i = 0; i < samplesRead; i++) {
      Serial.println(sampleBuffer[i]);
    }
    samplesRead = 0;
  }
}

void onPDMdata() {
  int bytesAvailable = PDM.available();
  PDM.read(sampleBuffer, bytesAvailable);
  samplesRead = bytesAvailable / 2; // 2 bytes por muestra
}
