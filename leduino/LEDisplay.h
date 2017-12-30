#ifndef LEDISPLAY_H
#define LEDISPLAY_H

#include <Arduino.h>
#include <FastLED.h>

#define DATA_PIN 5

enum LedOrientation {
  LEFT_TO_RIGHT,
  ZIG_ZAG
};

class LEDisplay {
  public: 
    LEDisplay(uint8_t ncols, uint8_t nrows);
    ~LEDisplay();

    void setColor(const uint8_t index, const CRGB color);
    void setPixel(uint8_t x, uint8_t y, CRGB color);
    void setPixelIdx(uint8_t x, uint8_t y, uint8_t idx);
    void setPixel(uint16_t index, CRGB color);
    void clearPixel(uint8_t x, uint8_t y);
    void hLine(uint8_t row, CRGB color);
    void vLine(uint8_t col, CRGB color);
    void rshiftRow(const uint8_t row);
    void rshift();    
    void lshiftRow(const uint8_t row);
    void lshift();
    boolean oddRow(const uint8_t row) const;
    boolean oddColumn(const uint8_t column) const;
    void setCursor(const uint16_t index);
    void writeRaw(const uint8_t size, uint8_t* data) const;
    
    void clear();
    void show();
    void fill(CRGB color);
    uint16_t numberOfLeds();

  private:
    uint8_t m_rows, m_cols;
    CRGB* leds;
    CRGB colorTable[256];
    LedOrientation ledOrientation;
    uint16_t cursor;

    uint16_t calculatePosition(uint8_t x, uint8_t y);
    boolean validCoords(uint8_t x, uint8_t y);
};

#endif
