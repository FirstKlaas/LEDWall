#include "buffer.hpp"

FrameBuffer::FrameBuffer(uint16_t numberOfLeds) {
  buffer = std::unique_ptr<uint8_t[]>(new uint8_t[numberOfLeds*3]{});
  size = numberOfLeds;
};

FrameBuffer& FrameBuffer::operator+=(const uint8_t data) {
  switch(data) {
    case FrameBuffer::Command::CMD_PAINT_PANEL:
      index = 0;
      break;
    default:
      if (frameCompleted()) {
        
      } else {
        buffer[index] = data;
        index++;
      };
  };
};
