#ifndef LEDISPLAY_H
#define LEDISPLAY_H

#include <Arduino.h>
#include <FastLED.h>

class LEDisplay {
  public: 
    LEDisplay(uint8_t ncols, uint8_t nrows);
    ~LEDisplay();

    void setPixel(uint8_t x, uint8_t y, CRGB color);
    void clear();
    void fill(CRGB color);
    uint16_t numberOfLeds();

  private:
    uint8_t m_rows, m_cols;
    CRGB* leds;

    uint16_t calculatePosition(uint8_t x, uint8_t y);
};

#endif
