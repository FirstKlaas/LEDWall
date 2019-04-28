#define DEBUG
#define FASTLED_ESP8266_RAW_PIN_ORDER
#include "FastLED.h"

#include <ESP8266WiFi.h>


#define PORT 3548
#define NUM_LEDS 49
#define DATA_PIN 0
//#define DATA_PIN D4

// COMMANDS
#define BYTES_PER_PIXEL      3
#define CMD_PAINT_PANEL    243

//FLAGS
#define UPDATE           2

const char* ssid        = "hackathon24";      
const char* password    = "tomdockle24";

const int16_t numberOfByte = NUM_LEDS * BYTES_PER_PIXEL;

uint8_t leds[numberOfByte];

WiFiServer wifiServer(PORT);

void setup() {
  #ifdef DEBUG
  Serial.begin(9600);
  #endif
  WiFi.hostname("LEDPanel-TWO");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    #ifdef DEBUG
    Serial.print(".");
    #endif
  }
  #ifdef DEBUG
  Serial.println(WiFi.localIP());
  #endif
  
  #ifdef DEBUG
  Serial.println("");
  #endif
  FastLED.addLeds<NEOPIXEL, DATA_PIN>((CRGB*)leds, NUM_LEDS);
  wifiServer.begin();
  FastLED.showColor(CRGB::Orange);
}

void loop() {  
  int16_t index = -1;
  unsigned long t1 = millis();
  
  WiFiClient client = wifiServer.available(); 
  if (client) {
    while (client.connected()) {
      #ifdef DEBUG
      //Serial.println("Client");
      #endif
      while (client.available()>0) {
        if (index < 0) {
          leds[0] = client.read();
          if (leds[0] == CMD_PAINT_PANEL) {
            #ifdef DEBUG
            Serial.println("BOF");
            #endif
            index = 0;
          } else {
            FastLED.showColor(CRGB::Blue);  
          }
        } else {
          leds[index++] = client.read();
          #ifdef DEBUG
          Serial.print(index-1); Serial.print(": "); Serial.println(leds[index-1]);
          #endif
              
          if (index == (numberOfByte-1)) {
            #ifdef DEBUG
            Serial.println("EOF");
            #endif

            if (leds[0] == CMD_PAINT_PANEL) {
              index = 0;
            }
            FastLED.show();
            index = -1;
          }
        }
      }
    }
  }
}
