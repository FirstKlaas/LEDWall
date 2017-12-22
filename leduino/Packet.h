#ifndef PACKET_H
#define PACKET_H

#define EOT 255 // End-Of-Transmission
#define STX 254 // Start-Of-Data
#define ETX 253 // End-Of-Data

#define STATE_CMD    0
#define STATE_LENGTH 1
#define STATE_DATA   2

#include "Arduino.h"
typedef struct {
  uint8_t cmd;
  uint8_t cmdLength;
  uint8_t data[32];
} Package;

typedef Package* PackagePtr;

typedef void (*PackageHandler) (PackagePtr pckPtr); 

class Commander {
  public:
    Commander();
    void setPackageHandler(PackageHandler handler);
    void addByte(uint8_t data);

  private:
    PackageHandler _handler;
    Package pkg;
    uint16_t _idx;
    uint8_t  _state;
};

#endif
