#include "buffer.hpp"

static const int pixelFormat = NEO_GRB + NEO_KHZ800;

void FrameBuffer::fillRGB(uint8_t red, uint8_t green, uint8_t blue)
{
    if (initialized())
    {
        pixels->fill(Adafruit_NeoPixel::Color(red, green, blue), 0, size());
    };
}

void FrameBuffer::fillHSV(uint16_t hue, uint8_t sat, uint8_t val)
{
    if (initialized())
    {
        pixels->fill(Adafruit_NeoPixel::ColorHSV(hue, sat, val), 0, size());
    };
}

void FrameBuffer::setTableColor(uint16_t index, uint8_t red, uint8_t green, uint8_t blue)
{
    getColorTable().setIndexColor(index, CRGB(red, green, blue));
}

/******************************************
 * Returns the size of the panel. The size
 * is equal to the number of connected LEDs
 ******************************************/
uint16_t FrameBuffer::size() const
{
    return m_width * m_height;
}

/******************************************
 * Initialises the framebuffer and sets
 * the correct size. The LED strip is 
 * initialised. This method has to be
 * called, before any operation on the 
 * LED strip can be performed.
 ******************************************/
void FrameBuffer::init(uint8_t pin, uint8_t width, uint8_t height)
{
    m_width = width;
    m_height = height;
    pixels = new Adafruit_NeoPixel(size(), pin, pixelFormat);
    pixels->begin();
}

void FrameBuffer::handleOperation(Operation op, uint8_t data[], uint8_t buffer_size) {
    switch (op)
    {
    case Operation::INIT_PANEL:        
        init(data[0], data[1], data[2]);
        break;

    case Operation::FILL_HSV:
        fillHSV(data[0] << 8 | data[1], data[2], data[3]);
        break;

    case Operation::FILL_RGB:
        fillRGB(data[0], data[1], data[2]);
        break;

    case Operation::SET_TABLE_COLOR:
        setTableColor(data[0] << 8 | data[1], data[2], data[3], data[4]);
        break;
        
    case Operation::SET_PIXEL_RGB:
        if (initialized()) {
            pixels->setPixelColor(data[0] << 8 | data[1], Adafruit_NeoPixel::Color(data[2], data[3], data[4]));
        };
        break;

    case Operation::SET_PIXEL_HSV:
        if (initialized()) {
            pixels->setPixelColor(data[0] << 8 | data[1], Adafruit_NeoPixel::ColorHSV(data[2] << 8 | data[3], data[4], data[5]));
        };
        break;

    case Operation::RESET_COLOUR_TABLE_CURSOR:
        getColorTable().resetIterator();
        break;

    default:
        break;
    }
}

/******************************************
 * Handles an incoming byte, which is not
 * one of command bytes.
 * 
 * What to to with the byte depends on
 * the current command. 
 ******************************************/
void FrameBuffer::handleData(uint8_t data)
{

    switch (m_current_command)
    {

    // If no command is set, ignore
    // the incoming data.
    case (Command::NOP):
        break;

    case (Command::CMD_BUFFERED_COMMAND):
        if (data == END_OF_COMMAND)
        {
            idleCommand();
            // Now handle the command
            handleOperation(static_cast<Operation>(cmd_buffer[0]), cmd_buffer+1, sizeof(cmd_buffer)-1);
        }
        else if (m_index >= sizeof(cmd_buffer))
        {
            // Command Buffer is full, but we did not receive
            // a end of command data.
            // This is an error situation, we cannot solve.
            // For the moment we will reset the index and set
            // the command to nop
            idleCommand();
        }
        else
        {
            // Still space left in the command buffer,
            // so let's add the data to the buffer
            cmd_buffer[m_index++] = data;
        };

    case (Command::CMD_STREAM_COLOR_TABLE):
        {
            ColorTable16 ct = getColorTable();

            // If space is left, add the data
            if (!ct.table_complete()) ct += data;

            // Now check, if still space is left. 
            // If not, reset the iterator and 
            // set mode to NOP
            if (ct.table_complete())
            {
                ct.resetIterator();
                m_current_command = Command::NOP;
                return; // Out of Range !
            };
        };
        break;

    case (Command::CMD_STREAM_PANEL16):
        if (frameCompleted() || !initialized())
        {
            idleCommand();
            return;
        }
        // Set the color based on an indexed color
        // The highest four bits define the index
        // for the first color and the lower four
        // bits define the index for the second
        // color.
        pixels->getPixels()[m_index] = getColorTable().getIndexColor((data >> 4) & 0xF);
        m_index++;
        pixels->getPixels()[m_index] = getColorTable().getIndexColor(data & 0xF);
        m_index++;
        
        // If this was the last byte of the frame,
        // update the leds.
        if (frameCompleted())
        {
            pixels->show();
            idleCommand();
        }
        break;

    case (Command::CMD_STREAM_PANEL):
        if (frameCompleted())
        {
            idleCommand();
            return; // Out of Range !
        };

        if (!initialized())
        {
            idleCommand();
            return; // Out of Range !
        };

        pixels->getPixels()[m_index] = data;
        m_index++;
        // If this was the last byte of the frame,
        // update the leds.
        if (frameCompleted())
        {
            pixels->show();
            idleCommand();
        }
        break;
        /**
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
    **/
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
FrameBuffer &FrameBuffer::operator+=(const uint8_t data)
{
    switch (data)
    {
    case Command::CMD_STREAM_PANEL:
        m_index = 0;
        m_current_command = Command::CMD_STREAM_PANEL;
        break;

    case Command::CMD_STREAM_COLOR_TABLE:
        getColorTable().resetIterator();
        m_current_command = Command::CMD_STREAM_COLOR_TABLE;
        break;

    case Command::CMD_BUFFERED_COMMAND:
        m_index = 0;
        m_current_command = Command::CMD_BUFFERED_COMMAND;
        break;

    default:
        handleData(data);
        break;
    };
    return *this;
};
