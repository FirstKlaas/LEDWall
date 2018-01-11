#include <Arduino.h>
#include <FastLED.h>

#define DATA_PIN           5
#define BYTES_PER_PIXEL    3
#define MAX_SERIAL_DELAY  100

uint8_t* leds;
unsigned long time;

uint8_t cmdbuffer[32];

void setup() {
  //FastLED.addLeds<NEOPIXEL, DATA_PIN>((CRGB*)leds, NUMBER_OF_LEDS);
  Serial.begin(1000000);
  delay(100);
  time = millis();  
}

void createPanel() {
  uint16_t size = ((cmdbuffer[0] << 0xFF) | cmdbuffer[1]);
  leds = (uint8_t*) malloc(size * BYTES_PER_PIXEL);
}

void loop() {
  
}
