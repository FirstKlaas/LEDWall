Color Classes
=============

For a LED project color manipulation is of course the most important
part. The WS2812b needs for every pixel the RGB values, where every
component is represented as byte [0;255]. From a artistic point of 
view the HSV color space is much more intuitive. Therefore this library
provides convenience classes to create, manipulate and convert classes
in RGB and HSV color space.

Color
-----

.. autoclass:: ledwall.components.Color
	:members:
	
RGBColor
--------

.. autoclass:: ledwall.components.RGBColor
	:members:
	
HSVColor
--------

.. autoclass:: ledwall.components.HSVColor
	:members:
	
