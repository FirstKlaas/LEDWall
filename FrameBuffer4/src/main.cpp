#include <Arduino.h>
#include "buffer.hpp"

#define MAX_SERIAL_DELAY    3000  // Maximum delay between transmitted data within one command in milliseconds

FrameBuffer panel;

void setup() {
  Serial.begin(BAUDRATE);
  while (!Serial) {};
}

void loop() {  
  while (true) {
    if (Serial.available() > 0) {
      panel += Serial.read();      
    };
  }
}
