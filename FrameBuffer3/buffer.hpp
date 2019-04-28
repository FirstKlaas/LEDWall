#ifndef BUFFER_HPP
#define BUFFER_HPP

#include <memory>

class FrameBuffer {
  typedef enum {
    NEW_FRAME=1,
    END_OF_FRAME=2,
    RESET_FRAME=3,
    ERROR_STATUS=9,
    WRITE=10
  } Status;

  typedef enum {
    CMD_PAINT_PANEL=243
  } Command;

private:
  std::unique_ptr<uint8_t[]> buffer;
  uint8_t  size;
  uint16_t index{0}; 
  
public:
  FrameBuffer() =delete;
  FrameBuffer(uint16_t numberOfLeds) {
    buffer = std::unique_ptr<uint8_t[]>(new uint8_t[numberOfLeds*3]{});
  };

  boolean frameCompleted() {
    return (index >= (size*3));
  }
  
  FrameBuffer& operator+=(const uint8_t data) {
    switch(data) {
      case FrameBuffer::Command::CMD_PAINT_PANEL:
        index = 0;
        break;
      default:
        if (frameCompleted()) {
          
        } else {
          buffer[index++] = data;
        };
    };
  };
};


#endif
