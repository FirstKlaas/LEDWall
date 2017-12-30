#include "Packet.h"
#include "LEDisplay.h"

#define CMD_SHOW              1
#define CMD_SETPIXEL          2
#define CMD_CLEARPIXEL        3
#define CMD_FILL              4
#define CMD_SET_PALETTE_ENTRY 5
#define CMD_SET_PIXEL_IDX     6

#define CMD_HLINE             7
#define CMD_VLINE             8
#define CMD_CLEAR             9
#define CMD_RSHIFT_ROW       10
#define CMD_LSHIFT_ROW       11
#define CMD_RSHIFT           12
#define CMD_LSHIFT           13

#define CMD_SET_CURSOR       20
#define CMD_WRITE_RAW        21


LEDisplay panel(7,7);
uint8_t line;
Commander cmd;

void cmdHandler(PackagePtr pkg) {
  switch(pkg->cmd) {
    case CMD_SETPIXEL:
      panel.setPixel(pkg->data[0],pkg->data[1],CRGB(pkg->data[2],pkg->data[3],pkg->data[4]));
      break;
    case CMD_SHOW:
      panel.show();
      break;
    case CMD_FILL:
      panel.fill(CRGB(pkg->data[0],pkg->data[1],pkg->data[2]));
      break;
    case CMD_SET_PALETTE_ENTRY:
      panel.setColor(pkg->data[0],CRGB(pkg->data[1],pkg->data[2],pkg->data[3]));
      break;
    case CMD_SET_PIXEL_IDX:
      panel.setPixelIdx(pkg->data[0],pkg->data[1],pkg->data[2]);
      break;
    case CMD_CLEAR:
      panel.clear();
      break;
    case CMD_RSHIFT_ROW:
      panel.rshiftRow(pkg->data[0]);
      break;
    case CMD_LSHIFT_ROW:
      panel.lshiftRow(pkg->data[0]);
      break;
    case CMD_RSHIFT:
      panel.rshift();
      break;
    case CMD_LSHIFT:
      panel.lshift();
      break;      
    case CMD_SET_CURSOR:
      panel.setCursor((pkg->data[0] << 8) | pkg->data[1]);
      break;
    case CMD_WRITE_RAW:
      panel.writeRaw(pkg->cmdLength, pkg->data);
      break;      
  }
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  delay(100);
  panel.setColor(0,CRGB::AliceBlue);
  panel.setColor(1,CRGB::Amethyst);
  panel.setColor(2,CRGB::DarkOrange);
 
  panel.clear();
  panel.show();
  
  cmd.setPackageHandler(cmdHandler);
}

void loop() {
  if (Serial.available()) {
    while(Serial.available()) cmd.addByte(Serial.read());
  }
}
