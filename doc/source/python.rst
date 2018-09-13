Python Library
==============

The python library provides modules and classes to manipulate the pixel colors
on the LED Display. I tried to design a pythonic API, which makes it very
intuitive to paint to the LED Display.

A very simple python script would look like this:

.. code-block:: python

    from ledwall.components import *

    # Create a new display instance. Using a SerialSender to
    # send the color data to the arduino.
    # Setting the desired framerate is 15
    d = Display(16,32, SerialSender(portName='/dev/ttyACM0', baudrate=1000000), framerate=15)

    # Defining a few basic colors
    red   = RGBColor.fromIntValues(255,0,0)
    green = RGBColor.fromIntValues(0,255,0)

    d.fill(green)
    d.setPixel(0,3,red)
    d.setPixel(14,23,red)

    d.update()


.. toctree::
    :hidden:

    components
    geometry

