#ifndef BUFFER_HPP
#define BUFFER_HPP

#include <memory>
#include <Arduino.h>
#include <Adafruit_NeoPixel.h>

class FrameBuffer {

  typedef enum {
    CMD_PAINT_PANEL=243
  } Command;

private:
  std::unique_ptr<uint8_t[]> buffer;
  uint8_t  size;
  uint16_t index; 
  Adafruit_NeoPixel *pixels;

  
public:
  FrameBuffer() =delete;
  FrameBuffer(uint16_t numberOfLeds);

  boolean frameCompleted() {
    return (index >= (size*3));
  };

  uint16_t getIndex() { return index; };

  FrameBuffer& operator+=(const uint8_t data);
};


#endif
