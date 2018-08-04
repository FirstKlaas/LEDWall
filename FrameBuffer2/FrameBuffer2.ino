#include <Arduino.h>
#include <FastLED.h>

#define DATA_PIN           5
#define BYTES_PER_PIXEL    3
#define MAX_SERIAL_DELAY  100

#define CMD_INIT_PANEL      1
#define CMD_CLEAR_PANEL     2
#define CMD_FILL_PANEL      3
#define CMD_PAINT_PANEL     4

#define NODEBUG

CRGB leds[100];
unsigned long time;
uint8_t numberOfLeds = 100;

uint8_t cmdbuffer[16];

void setup() {
  
  Serial.begin(115200);
  Serial.setTimeout(60000);
  delay(3000);
  time = millis();  

  FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, 100);
  FastLED.showColor(CRGB::Yellow);
}

void initPanel() {
  /**
  if (cmdbuffer[0] != CMD_INIT_PANEL) return;
  if (leds != NULL) free(leds); 
  
  //0 = WIDTH
  //1 = HEIGHT
  
  Serial.readBytes(cmdbuffer,2);
  width  = cmdbuffer[0];
  height = cmdbuffer[1];
  
  numberOfLeds = width * height;
  
  #ifdef DEBUG
  Serial.print("Init ");
  Serial.print(width);
  Serial.print(";");
  Serial.println(height);
  #endif
  
  leds = (CRGB*)malloc(numberOfLeds * sizeof(CRGB));
  FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, numberOfLeds);

  FastLED.showColor(CRGB::Green);
  **/
}

void clearPanel() {
  if (leds == NULL) return; 
  if (cmdbuffer[0] != CMD_CLEAR_PANEL) return;

  FastLED.showColor(CRGB::White);
}

void fillPanel() {
  if (leds == NULL) return; 
  if (cmdbuffer[0] != CMD_FILL_PANEL) return;

  Serial.readBytes(cmdbuffer,3);
  FastLED.showColor(CRGB(cmdbuffer[0],cmdbuffer[1],cmdbuffer[2])); 
}

void paintPanel() {
  if (leds == NULL) return; 
  if (cmdbuffer[0] != CMD_PAINT_PANEL) return;
  Serial.readBytes((uint8_t*) leds,numberOfLeds * 3);
  #ifdef DEBUG
  for (int i=0; i< (numberOfLeds * 3); i++) {
      Serial.print(leds[i]);Serial.print(";");
      if (i % 21 == 0) {
        Serial.println("");      
      }
  }
  Serial.println(" => Frame complete");
  #endif
  FastLED.show();
  
}

void loop() {
  Serial.readBytes(cmdbuffer,1);
  #ifdef DEBUG
  Serial.print("Command: ");
  Serial.println(cmdbuffer[0]);
  #endif
  switch(cmdbuffer[0]) {
    case CMD_INIT_PANEL: 
      initPanel(); 
      break;
      
    case CMD_CLEAR_PANEL:
      clearPanel();
      break;
      
    case CMD_FILL_PANEL:
      fillPanel();
      break;

    case CMD_PAINT_PANEL:
      paintPanel();
      break;
  } 
}
