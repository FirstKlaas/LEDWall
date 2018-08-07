#include <Arduino.h>
#include <FastLED.h>

#define DATA_PIN             5
#define BYTES_PER_PIXEL      3

#define MAX_SERIAL_DELAY   500  // Maximum delay between transmitted data within one command in milliseconds

#define CMD_INIT_PANEL       1
#define CMD_CLEAR_PANEL      2
#define CMD_FILL_PANEL       3
#define CMD_PAINT_PANEL      4

#define DEBUG

uint8_t leds[300];
unsigned long time;
uint8_t numberOfLeds = 100;

uint8_t cmdbuffer[16];

void setup() {
  
  Serial.begin(115200);
  //Serial.setTimeout(6000);
  delay(500);
  FastLED.addLeds<NEOPIXEL, DATA_PIN>((CRGB*)leds, 100);
  FastLED.showColor(CRGB::Yellow);
}


void loop() {
  int16_t index = -1;
  unsigned long t1 = millis();
  //&& ((millis()-t1) < MAX_SERIAL_DELAY)
  while (index < (numberOfLeds*3) ) {
    if (Serial.available() > 0) {
      if (index < 0) {
        leds[0] = Serial.read();
        //Serial.print("New frame start. Magic number is "); Serial.println(leds[0]);
        if (leds[0] == CMD_PAINT_PANEL) {
          index = 0;
        } else {
          //Serial.println("Wrong command");
          FastLED.showColor(CRGB::Blue);  
        }
      } else {
        leds[index++] = Serial.read();
      }  
    }
  }
  //Serial.print("Index: ");Serial.println(index);
  if (index == (numberOfLeds*3)) {
    //Serial.print("Time: ");Serial.println(millis()-t1);
    FastLED.show();    
  } else {
    FastLED.showColor(CRGB::Black);
  }
}
