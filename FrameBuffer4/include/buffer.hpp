#ifndef BUFFER_HPP
#define BUFFER_HPP

#include <memory>
#include <Arduino.h>
#include <Adafruit_NeoPixel.h>

class FrameBuffer {

  typedef enum {
    NOP=0, 
    CMD_INIT_PANEL=234,
    CMD_PAINT_PANEL=243,
    END_OF_COMMAND=254
  } Command;

private:
  std::unique_ptr<uint8_t[]> buffer;
  uint8_t  m_width;
  uint8_t m_height;
  uint16_t index; 
  uint8_t cmd_buffer[8];
  Adafruit_NeoPixel *pixels;
  FrameBuffer::Command currentCommand;

  void handleData(uint8_t data);
  
public:
  FrameBuffer() =delete;
  FrameBuffer();

  void init(uint8_t pin, uint8_t width, uint8_t height);

  boolean frameCompleted() {
    return (index >= (size()*3));
  };

  uint16_t size() const;
  uint16_t getIndex() { return index; };

  FrameBuffer& operator+=(const uint8_t data);
};


#endif
