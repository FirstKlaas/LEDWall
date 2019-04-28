#include <Arduino.h>
//#include <HardwareSerial.h>
#include <FastLED.h>

#include "buffer.hpp"


#define DATA_PIN             4
#define BAUDRATE           9600
#define MAX_SERIAL_DELAY   3000  // Maximum delay between transmitted data within one command in milliseconds

#define BYTES_PER_PIXEL      3
#define CMD_PAINT_PANEL    243

#define NODEBUG

#define NEW_FRAME            1
#define END_OF_FRAME         2
#define RESET_FRAME          3
#define ERROR_STATUS         9


const uint8_t numberOfLeds  = 49;
const int16_t numberOfByte = numberOfLeds * BYTES_PER_PIXEL;

uint8_t leds[numberOfByte];
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
  while (index < numberOfByte) { // && ((millis()-t1) < MAX_SERIAL_DELAY)) {
    if (Serial.available() > 0) {
      if (index < 0) {
        leds[0] = Serial.read();
        if (leds[0] == CMD_PAINT_PANEL) {
          index = 0;
          Serial.print(NEW_FRAME);
        }
      } else {
        leds[index] = Serial.read();
        if (leds[index] == CMD_PAINT_PANEL) {
          index = 0;
          Serial.print(RESET_FRAME);
          Serial.flush();
        } else {
          index++;
        }
      }
        
    }
  }

  if (index >= (numberOfByte)) {
    FastLED.show();    
    Serial.print(END_OF_FRAME);
    Serial.print(ERROR_STATUS);
    Serial.flush();
  }
}
