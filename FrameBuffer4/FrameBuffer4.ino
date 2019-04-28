#include <Arduino.h>

#define FASTLED_ALLOW_INTERRUPTS 0
#include <FastLED.h>

#include "buffer.hpp"

#define DATA_PIN              4
#define BAUDRATE        1000000
#define MAX_SERIAL_DELAY   3000  // Maximum delay between transmitted data within one command in milliseconds

const uint8_t numberOfLeds  = 49;

FrameBuffer panel(numberOfLeds);

void setup() {
  Serial.begin(BAUDRATE);
  delay(500);
  FastLED.addLeds<NEOPIXEL, DATA_PIN>((CRGB*) panel.ptr(), numberOfLeds);
  delay(500);
  FastLED.showColor(CRGB::Yellow);
}

void loop() {
  while (true) {
    if (Serial.available() > 0) {
      panel += Serial.read();
      
      if (panel.frameCompleted()) {
        FastLED.show();
      }
    };
  }
}
