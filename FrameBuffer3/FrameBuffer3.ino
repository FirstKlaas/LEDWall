#include <Arduino.h>
#include <FastLED.h>

#define DATA_PIN              5
#define BAUDRATE         500000
#define MAX_SERIAL_DELAY   3000  // Maximum delay between transmitted data within one command in milliseconds

#define BYTES_PER_PIXEL      3
#define CMD_PAINT_PANEL    243

#define NODEBUG

const uint8_t numberOfLeds  = 100;
const int16_t numberOfByte = numberOfLeds * BYTES_PER_PIXEL;

uint8_t leds[numberOfByte];
unsigned long time;

uint8_t cmdbuffer[16];

void setup() {
  Serial.begin(BAUDRATE);
  delay(500);
  FastLED.addLeds<NEOPIXEL, DATA_PIN>((CRGB*)leds, numberOfLeds);
  delay(500);
  FastLED.showColor(CRGB::Yellow);
}


void loop() {
  int16_t index = -1;
  unsigned long t1 = millis();
  while (index < numberOfByte && ((millis()-t1) < MAX_SERIAL_DELAY)) {
    if (Serial.available() > 0) {
      if (index < 0) {
        leds[0] = Serial.read();
        if (leds[0] == CMD_PAINT_PANEL) {
          index = 0;
        } else {
          FastLED.showColor(CRGB::Blue);  
        }
      } else {
        leds[index++] = Serial.read();
        if (leds[0] == CMD_PAINT_PANEL) {
          index = 0;
        }
      }  
    }
  }
  
  if (index == (numberOfByte)) {
    FastLED.show();    
  } else {
    FastLED.showColor(CRGB::Black);
  }
}
