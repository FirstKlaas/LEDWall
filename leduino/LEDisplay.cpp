#include "LEDisplay.h"

LEDisplay::LEDisplay(uint8_t ncols, uint8_t nrows):
m_rows(nrows), m_cols(ncols)
{
  leds = malloc(sizeof(CRGB) * ncols * nrows);
}

LEDisplay::~LEDisplay() {
  free(leds);
}

uint16_t LEDisplay::calculatePosition(uint8_t x, uint8_t y) {
  if (x >= m_cols || y >= m_rows) return -1;
  return x*y;
}

void LEDisplay::setPixel(uint8_t x, uint8_t y, CRGB color) {
  const uint16_t pos = calculatePosition(x,y);
  if (pos < 0) return;
  leds[pos] = color;  
}

uint16_t LEDisplay::numberOfLeds() {
  return m_cols * m_rows;
}

void LEDisplay::fill(CRGB color) {
  for (uint16_t i=0; i< numberOfLeds(); i++) {
    leds[i] = color; 
  }
}

void LEDisplay::clear() {
  fill(CRGB::Black);
}

