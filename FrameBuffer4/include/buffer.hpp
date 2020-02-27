#ifndef BUFFER_HPP
#define BUFFER_HPP

#include <memory>
#include <Arduino.h>
#include <Adafruit_NeoPixel.h>

#define END_OF_COMMAND 245
#define EOC 245

typedef enum {
  NONE=0,
  INIT_PANEL=1,
  FILL_RGB=2,
  FILL_HSV=3,
  SET_TABLE_COLOR=4,
  SET_PIXEL_RGB=5,
  SET_PIXEL_HSV=6
} Operation;

typedef enum {
  NOP = 254, 
  CMD_STREAM_PANEL = 243,
  CMD_STREAM_PANEL16 = 244,
  CMD_STREAM_COLOR_TABLE = 253,
  CMD_BUFFERED_COMMAND = 251
} Command;

struct CRGB {
	union {
		struct {
            union {
                uint8_t r;
                uint8_t red;
            };
            union {
                uint8_t g;
                uint8_t green;
            };
            union {
                uint8_t b;
                uint8_t blue;
            };
        };
		uint8_t raw[3];
	};

  /// Array access operator to index into the crgb object
	inline uint8_t& operator[] (uint8_t x) __attribute__((always_inline))
  {
    return raw[x];
  }

  /// Array access operator to index into the crgb object
  inline const uint8_t& operator[] (uint8_t x) const __attribute__((always_inline))
  {
    return raw[x];
  }

  // default values are UNINITIALIZED
	inline CRGB() __attribute__((always_inline))
  {
  }

  /// allow construction from R, G, B
  inline CRGB( uint8_t ir, uint8_t ig, uint8_t ib)  __attribute__((always_inline))
  : r(ir), g(ig), b(ib)
  {
  }

  /// allow construction from 32-bit (really 24-bit) bit 0xRRGGBB color code
  inline CRGB( uint32_t colorcode)  __attribute__((always_inline))
  : r((colorcode >> 16) & 0xFF), g((colorcode >> 8) & 0xFF), b((colorcode >> 0) & 0xFF)
  {
  }

  inline operator uint32_t() const { return (red << 16 | green << 8 | blue); };

  /// allow assignment from R, G, and B
	inline CRGB& setRGB (uint8_t nr, uint8_t ng, uint8_t nb) __attribute__((always_inline))
  {
    r = nr;
    g = ng;
    b = nb;
    return *this;
  }
};


class ColorTable16 {

private:
  union {
    CRGB colors[16];
    uint8_t color_raw[sizeof(CRGB)*16];
  };
  uint8_t m_iterator; 

public:
  ColorTable16() : m_iterator(0) {};

  inline void setIndexColor(uint8_t index, CRGB color) {
    if (index > 15) return;
    colors[index] = color;
  }

  bool table_complete() {
    return (m_iterator >= sizeof(color_raw));  
  }

  inline const CRGB& getIndexColor(uint8_t index) const {
    return colors[index];
  }

  inline const CRGB& operator[] (uint8_t index) const {
    return getIndexColor(index);
  }

  inline CRGB& operator[] (uint8_t index) {
    return colors[index];
  }

  inline uint8_t size() { return 16; };

  inline void resetIterator() {
    m_iterator = 0;
  }

  inline ColorTable16& operator+=(uint8_t data) {
    if (!table_complete()) { 
      color_raw[m_iterator++] = data;
    };
    return *this;
  }
};

class FrameBuffer {

private:
  uint8_t  m_width;
  uint8_t m_height;
  uint16_t m_index; 
  uint8_t cmd_buffer[8];
  Adafruit_NeoPixel *pixels;
  Command m_current_command;
  Operation m_current_operation;
  ColorTable16 *color_table;

  void handleData(uint8_t data);

  ColorTable16& getColorTable() {
    if(!color_table) {
      color_table = new ColorTable16();
    };
    return *color_table;
  };

  void handleOperation(Operation op, uint8_t data[], uint8_t buffer_size);

  void idleCommand() {
    m_index = 0;
    m_current_command = Command::NOP;
  };

public:
  FrameBuffer()
  :m_width(0), m_height(0), m_index(0), m_current_command(Command::NOP), color_table(nullptr) 
  {};

  void init(uint8_t pin, uint8_t width, uint8_t height);
  void fillRGB(uint8_t red=0, uint8_t green=0, uint8_t blue=0);
  void fillHSV(uint16_t hue, uint8_t sat=255, uint8_t val=255);
  bool initialized() { return size() > 0; }
  void setTableColor(uint16_t index, uint8_t red, uint8_t green, uint8_t blue);

  boolean frameCompleted() {
    return (m_index >= (size()*3));
  };

  uint16_t size() const;
  uint16_t getIndex() { return m_index; };
  void show() { pixels->show(); };

  FrameBuffer& operator+=(const uint8_t data);  
};

#endif
