#include "buffer.hpp"

static const int pixelFormat = NEO_GRB + NEO_KHZ800;

void FrameBuffer::fillRGB(uint8_t red, uint8_t green, uint8_t blue) {
  if (initialized()) {
    pixels->fill(Adafruit_NeoPixel::Color(red, green, blue), 0, size());
  };
}

void FrameBuffer::fillHSV(uint16_t hue, uint8_t sat, uint8_t val) {
  if (initialized()) {
    pixels->fill(Adafruit_NeoPixel::ColorHSV(hue, sat, val), 0, size());
  };
}

void FrameBuffer::setTableColor(uint8_t index, uint8_t red, uint8_t green, uint8_t blue) 
{
  // We only have 16 colors (index 0 to 15).
  // So any value higher than 15 is out of range.
  if (index > 15) return;

  // Make sure, the memory for the color 
  // table is allocated
  if (!color_table) {
    color_table = new ColorTable16();
  }
  // color_table[index] = CRGB(red, green , blue)
  color_table->setIndexColor(index, CRGB(red, green , blue));
}

/******************************************
 * Returns the size of the panel. The size
 * is equal to the number of connected LEDs
 ******************************************/  
uint16_t FrameBuffer::size() const {
  return m_width * m_height;
}

/******************************************
 * Initialises the framebuffer and sets
 * the correct size. The LED strip is 
 * initialised. This method has to be
 * called, before any operation on the 
 * LED strip can be performed.
 ******************************************/  
void FrameBuffer::init(uint8_t pin, uint8_t width, uint8_t height) {
  m_width = width;
  m_height = height; 
  pixels = new Adafruit_NeoPixel(size(), pin, pixelFormat);
  pixels->begin();
}  

/******************************************
 * Handles an incoming byte, which is not
 * one of command bytes.
 * 
 * What to to with the byte depends on
 * the current command. 
 ******************************************/  
void FrameBuffer::handleData(uint8_t data) {

  switch(m_current_command) {

    // If no command is set, ignore 
    // the incoming data.
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

    case(Command::CMD_SET_TABLE_COLOR):
      cmd_buffer[m_index++] = data;
      if (m_index == 4) {
        setTableColor(cmd_buffer[0],cmd_buffer[1],cmd_buffer[2],cmd_buffer[3]);
        memset(cmd_buffer,0,4);
        m_current_command = Command::NOP;
      };
      break;
    
    case(Command::CMD_PAINT_PANEL):
      if (frameCompleted()) return; // Out of Range !
      if (!initialized()) return;
      
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


/******************************************
 * Defines the unary add operator, to add 
 * a byte to the buffer. 
 * This method first check, if the added
 * byte is a command byte. If so, the
 * current command is set and the index
 * is set to zeor. If the byte is not a
 * command byte, the byte is handed over
 * to the handleData method.
 ******************************************/  
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
