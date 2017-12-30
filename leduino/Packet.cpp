#include "Packet.h"

Commander::Commander()
: _handler(NULL),_idx(255),_state(STATE_CMD)
{
  
}

void Commander::setPackageHandler(PackageHandler handler) {
  _handler = handler;
}

void Commander::addByte(uint8_t val) {
  switch(_state) {
    case STATE_CMD: 
      pkg.cmd = val;
      _state = STATE_LENGTH;
      break;
    case STATE_LENGTH:
      pkg.cmdLength = val;
      _idx   = 0;
      _state = STATE_DATA;
      break;
    case STATE_DATA:
      pkg.data[_idx] = val;
      _idx++;
      break;  
  }
  if (_idx == pkg.cmdLength) {
    if (_handler) {
      _handler(&pkg);
    }
    _idx = 255;
    _state = STATE_CMD;
  }    
}


