LED Wall
========

An interactive LED matrix based on WS2812b LEDs
-----------------------------------------------

The Idea
^^^^^^^^
A LED Matrix which can be used as a display to play games
or to show different information (like the current weather
conditions)

The Architecture
^^^^^^^^^^^^^^^^

The main ingredients are:

* Raspberry PI (Version 2 or 3 will do)
* Arduino Uno (for wireless panels use a NodeMCU)
* LW2812b LED Stripes

Python
^^^^^^

For easy color manipulation as well as different hardware setups.
I wrote a python library. To get started, read the documentation
of the :class:`~ledwall.components.Display` class.

Contents
^^^^^^^^

.. toctree::

   getting_started
   python
   arduino-mqtt

Indices and tables
^^^^^^^^^^^^^^^^^^

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

