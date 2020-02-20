#include <Arduino.h>

#define FASTLED_ALLOW_INTERRUPTS 0
#include "buffer.hpp"

#define DATA_PIN              4
#define MAX_SERIAL_DELAY   3000  // Maximum delay between transmitted data within one command in milliseconds

const uint8_t numberOfLeds  = 49;

FrameBuffer panel;

void setup() {
  Serial.begin(BAUDRATE);
  while (!Serial) {};
  delay(500);
  panel.init(DATA_PIN, 7, 7); 
  panel.fillRGB(0,255,255); 
}

void loop() {
  while (true) {
    if (Serial.available() > 0) {
      panel += Serial.read();      
    };
  }
}
