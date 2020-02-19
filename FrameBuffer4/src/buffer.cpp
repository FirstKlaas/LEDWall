#include "buffer.hpp"

static const int pixelFormat = NEO_GRB + NEO_KHZ800;


/******************************************
 * Constructor
 ******************************************/  
FrameBuffer::FrameBuffer(): 
  index(0), m_width(0), m_height(0), currentCommand(FrameBuffer::Command::NOP) 
{};

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
  switch (currentCommand) {

    case(FrameBuffer::Command::CMD_INIT_PANEL):
      cmd_buffer[index++] = data;
      if (index == 3) {
        // Pin and width and height provided
        init(cmd_buffer[0], cmd_buffer[1], cmd_buffer[2]);
        memset(cmd_buffer,0,3);
      };    
      break;
    
    case(FrameBuffer::Command::CMD_PAINT_PANEL):
      if (frameCompleted()) return; // Out of Range !
      
      pixels->getPixels[index++] = data;
      if (frameCompleted()) {
        pixels->show();
      }
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
    case FrameBuffer::Command::CMD_PAINT_PANEL:
      index = 0;
      currentCommand = FrameBuffer::Command::CMD_PAINT_PANEL;
      break;
    case FrameBuffer::Command::CMD_INIT_PANEL:
      index = 0;
      currentCommand = FrameBuffer::Command::CMD_INIT_PANEL;
      break;
    default:
      handleData(data);
  };
  return *this;
};
