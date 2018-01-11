#include <Arduino.h>
#include <FastLED.h>

#define DATA_PIN           5
#define BYTES_PER_PIXEL    3
#define NUMBER_OF_LEDS    49
#define MAX_SERIAL_DELAY  100

uint8_t leds[NUMBER_OF_LEDS*BYTES_PER_PIXEL];
uint16_t index;
unsigned long time;

void setup() {
  FastLED.addLeds<NEOPIXEL, DATA_PIN>((CRGB*)leds, NUMBER_OF_LEDS);
  Serial.begin(1000000);
  delay(100);
  index = 0;
  time = millis();  
}

void loop() {
  if (Serial.available()) {
    if (millis() - time > MAX_SERIAL_DELAY) {
      index = 0;
    }
    while(Serial.available()) {
      leds[index] = Serial.read();
      index++;
      if (index == (NUMBER_OF_LEDS*BYTES_PER_PIXEL)) {
        FastLED.show();
        index = 0;        
      }
    }
    time = millis();
  }
}
