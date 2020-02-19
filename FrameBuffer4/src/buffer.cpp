#include "buffer.hpp"

FrameBuffer::FrameBuffer(uint16_t numberOfLeds): index(0)  
{
  size = numberOfLeds;
};

FrameBuffer& FrameBuffer::operator+=(const uint8_t data) {
  switch(data) {
    case FrameBuffer::Command::CMD_PAINT_PANEL:
      index = 0;
      break;
    default:
      if (frameCompleted()) {
        pixels->show();    
      } else {
        pixels->getPixels[index] = data;
        index++;
      };
  };
  return *this;
};
