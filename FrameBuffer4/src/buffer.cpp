#include "buffer.hpp"

static const int pixelFormat = NEO_GRB + NEO_KHZ800;

void FrameBuffer::fillRGB(uint8_t red, uint8_t green, uint8_t blue) {
  pixels->fill(Adafruit_NeoPixel::Color(red, green, blue), 0, size());
}

void FrameBuffer::fillHSV(uint16_t hue, uint8_t sat, uint8_t val) {
  pixels->fill(Adafruit_NeoPixel::ColorHSV(hue, sat, val), 0, size());
}

uint16_t FrameBuffer::size() const {
  return m_width * m_height;
}

void FrameBuffer::init(uint8_t pin, uint8_t width, uint8_t height) {
  m_width = width;
  m_height = height; 
  pixels = new Adafruit_NeoPixel(size(), pin, pixelFormat);
  pixels->begin();
}
  
void FrameBuffer::handleData(uint8_t data) {

  switch(m_current_command) {

    case(Command::NOP):
      break;

    case(Command::CMD_INIT_PANEL):
      cmd_buffer[m_index++] = data;
      if (m_index == 3) {
        // Pin and width and height provided
        init(cmd_buffer[0], cmd_buffer[1], cmd_buffer[2]);
        memset(cmd_buffer,0,3);
        m_current_command = Command::NOP;
      };    
      break;
    
    case(Command::CMD_PAINT_PANEL):
      if (frameCompleted()) return; // Out of Range !
      
      pixels->getPixels()[m_index] = data;
      m_index++;
      if (frameCompleted()) {
        pixels->show();
        m_current_command = Command::NOP;
      }
      break;

    case(Command::CMD_FILL_RGB):
      cmd_buffer[m_index++] = data;
      if (m_index == 3) {
        // We have a r, g and b value
        fillRGB(cmd_buffer[0], cmd_buffer[1], cmd_buffer[2]);
        memset(cmd_buffer,0,3);
        m_current_command = Command::NOP;
      };    
      break;

    case(Command::CMD_FILL_HSV):
      cmd_buffer[m_index++] = data;
      if (m_index == 4) {
        // We have a hue, saturation and value
        fillHSV(cmd_buffer[0] << 8 | cmd_buffer[1], cmd_buffer[2], cmd_buffer[3]);
        memset(cmd_buffer,0,4);
        m_current_command = Command::NOP;
      };    
      break;
      
  };
}

FrameBuffer& FrameBuffer::operator+=(const uint8_t data) {
  switch(data) {
    case Command::CMD_PAINT_PANEL:
      m_index = 0;
      m_current_command = Command::CMD_PAINT_PANEL;
      break;

    case Command::CMD_INIT_PANEL:
      m_index = 0;
      m_current_command = Command::CMD_INIT_PANEL;
      break;

    case Command::CMD_FILL_RGB:
      m_index = 0;
      m_current_command = Command::CMD_FILL_RGB;
      break;

    case Command::CMD_FILL_HSV:
      m_index = 0;
      m_current_command = Command::CMD_FILL_HSV;
      break;

    default:
      handleData(data);
      break;
  };
  return *this;
};
