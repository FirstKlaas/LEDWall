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
  }
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  delay(100);
  for (uint8_t i=0; i<=100; i++) {
    panel.setColor(i,CRGB( random(255), random(255), 0));
  }
  panel.setColor(0,CRGB::Blue);
  panel.setColor(1,CRGB::Red);
  panel.setColor(2,CRGB::Green);
  
  
  panel.clear();
  panel.show();
  
  cmd.setPackageHandler(cmdHandler);
  /**
  cmd.addByte(CMD_FILL);
  cmd.addByte(3);
  cmd.addByte(200);
  cmd.addByte(10);
  cmd.addByte(10);
  
  cmd.addByte(CMD_SETPIXEL);
  cmd.addByte(5);
  cmd.addByte(1);
  cmd.addByte(2);
  cmd.addByte(128);
  cmd.addByte(0);
  cmd.addByte(128);

  cmd.addByte(CMD_SETPIXEL);
  cmd.addByte(5);
  cmd.addByte(5);
  cmd.addByte(5);
  cmd.addByte(128);
  cmd.addByte(0);
  cmd.addByte(128);

  cmd.addByte(CMD_SHOW);
  cmd.addByte(0);
  */  
}

void setTestPixel(uint8_t idx) {
  cmd.addByte(CMD_SETPIXEL);
  cmd.addByte(5);
  cmd.addByte(idx);
  cmd.addByte(0);
  cmd.addByte(255);
  cmd.addByte(0);
  cmd.addByte(128);

  cmd.addByte(CMD_SHOW);
  cmd.addByte(0);
}

void loop() {
  if (Serial.available()) {
    //cmd.addByte(Serial.read());
    int data = Serial.read();
    setTestPixel(data & 0xff);
  }
}

void animate() {
  for (uint8_t i=0; i<7; i+=2) {
    panel.rshiftRow(i);
    panel.setPixelIdx(0,i,random(100));
  }
  for (uint8_t i=1; i<7; i+=2) {
    panel.lshiftRow(i);
    panel.setPixel(6,i,CRGB( random(255), random(255),random(255)));
  }
  
  panel.show();
  delay(500);
}
