#include "LEDisplay.h"

LEDisplay::LEDisplay(uint8_t ncols, uint8_t nrows):
m_rows(nrows), m_cols(ncols), ledOrientation(LEFT_TO_RIGHT)
{
  leds = malloc(sizeof(CRGB) * ncols * nrows);
  clear();
  FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, numberOfLeds());
}

LEDisplay::~LEDisplay() {
  free(leds);
}

uint16_t LEDisplay::calculatePosition(uint8_t x, uint8_t y) {
  if (x >= m_cols || y >= m_rows) return 0;
  if (ledOrientation == LEFT_TO_RIGHT) return x+(y*m_cols);
  // ZIG_ZAG
  return (m_cols-x-1) + (y*m_cols);
}

void LEDisplay::setPixel(uint8_t x, uint8_t y, CRGB color) {
  if (!validCoords(x,y)) return; 
  const uint16_t pos = calculatePosition(x,y);
  leds[pos] = color;  
}

void LEDisplay::setPixel(uint16_t index, CRGB color) {
  if (index < numberOfLeds()) {
    leds[index] = color;
  }
}

void LEDisplay::clearPixel(uint8_t x, uint8_t y) {
  setPixel(x,y, CRGB::Black);
}

void LEDisplay::show() {
  FastLED.show();
}

uint16_t LEDisplay::numberOfLeds() {
  return m_cols * m_rows;
}

void LEDisplay::fill(CRGB color) {
  for (uint16_t i=0; i< numberOfLeds(); i++) {
    leds[i] = color; 
  }
}

void LEDisplay::hLine(uint8_t row, CRGB color) {
  if (!validCoords(0,row)) return; 
  uint16_t index = calculatePosition(0,row);
  for (int i=0; i<m_cols; i++) {
    leds[index++] = color;
  }
}

void LEDisplay::lshiftRow(const uint8_t row) {
  if (!validCoords(0,row)) return;
  uint16_t index = calculatePosition(0,row);  
  memcpy(&leds[index],&leds[index+1],sizeof(CRGB) * (m_cols-1));  
}

void LEDisplay::rshiftRow(const uint8_t row) {
  if (!validCoords(0,row)) return;
  uint16_t index = calculatePosition(m_cols-1,row);
  
  for (uint8_t i = (m_cols-1); i>0; i--) {
    memcpy(&leds[index],&leds[index-1],sizeof(CRGB));
    index--;
  }
  
  leds[index] = CRGB::Black;  
}

boolean LEDisplay::validCoords(uint8_t x, uint8_t y) {
  return x < m_cols && y < m_rows;
}

void LEDisplay::setColor(const uint8_t index, const CRGB color) {
  colorTable[index] = color;
}

void LEDisplay::setPixelIdx(uint8_t x, uint8_t y, uint8_t idx) {
  setPixel(x,y,colorTable[idx]);
}

void LEDisplay::vLine(uint8_t col, CRGB color) {
  if (!validCoords(col,0)) return; 
  uint16_t index = calculatePosition(col,0);
  for (int i=0; i<m_rows; i++) {
    leds[index] = color;
    index += m_cols;
  }
}

boolean LEDisplay::oddRow(const uint8_t row) const {
  return (row & 1);  
}

boolean LEDisplay::oddColumn(const uint8_t column) const {
  return (column & 1);  
}
    
void LEDisplay::clear() {
  fill(CRGB::Black);
}

