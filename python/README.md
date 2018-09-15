# LED Wall Python Library

A simple but powerful python library to manipulate WS2812b LED panel.
Panels cand be connected via USB cable or accessed via UDP. This library only supports Python 3 but is OS independent.

The library is intended to be used in conjunction with aa arduino or nodemcu tat controls a bunch of LEDs. Of course, you can write sketches to controll the LEDs directly in c using the arduino ide. But using python on a raspberry or some other computer will offer you more flexibility and speed in development. Also, you can leverage from wide range of existing python libraries. With just a few lines of code, you can integrate gamepads using the awesome inputs [library](https://pypi.org/project/inputs/).

For more information, examples, installation guides and the arduino/nodemcu sketches checkout my git [repository](https://github.com/FirstKlaas/LEDWall).

Also an [online documentation](https://ledwall.readthedocs.io/en/latest/) for the library is available on `readthedocs <https://readthedocs.org>`_.

## Example script

The following script shows the basic usage of the library. I tried to keep things pythonic.

```python
import ledwall.components as comp

# Create a new display instance. Using a SerialSender to
# send the color data to the arduino.
# Setting the desired framerate is 15
s = comp.SerialSender(portName='/dev/ttyACM0', baudrate=1000000)
d = comp.Display(16,32, s, framerate=15)

# Defining a few basic colors
red   = comp.RGBColor.fromIntValues(255,0,0)
green = comp.RGBColor.fromIntValues(0,255,0)

d.fill(green)
d.setPixel(0,3,red)
d.setPixel(14,23,red)

d.update()
```
