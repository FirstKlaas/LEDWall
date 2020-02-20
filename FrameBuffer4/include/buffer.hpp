#ifndef BUFFER_HPP
#define BUFFER_HPP

#include <memory>
#include <Arduino.h>
#include <Adafruit_NeoPixel.h>

typedef enum {
  NOP=0, 
  CMD_INIT_PANEL=234,
  CMD_PAINT_PANEL=243,
  CMD_FILL_RGB=246,
  CMD_FILL_HSV=248
} Command;

class FrameBuffer {

private:
  uint8_t  m_width;
  uint8_t m_height;
  uint16_t m_index; 
  uint8_t cmd_buffer[8];
  Adafruit_NeoPixel *pixels;
  Command m_current_command;

  void handleData(uint8_t data);

public:
  FrameBuffer(): m_width(0), m_height(0), m_index(0), m_current_command(Command::NOP) {};

  void init(uint8_t pin, uint8_t width, uint8_t height);
  void fillRGB(uint8_t red=0, uint8_t green=0, uint8_t blue=0);
  void fillHSV(uint16_t hue, uint8_t sat=255, uint8_t val=255);

  boolean frameCompleted() {
    return (m_index >= (size()*3));
  };

  uint16_t size() const;
  uint16_t getIndex() { return m_index; };
  void show() { pixels->show(); };

  FrameBuffer& operator+=(const uint8_t data);  
};


#endif
