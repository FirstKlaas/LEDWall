Python Library
==============

Getting Started
---------------

The python library provides modules and classes to manipulate the pixel colors
on the LED Panel. I tried to design a pythonic API, which makes it very intuitive to paint to the LED panel.

A very simple python script woul look like this:

.. code-block:: python
    
    from ledwall.components import Display

    # Create a new display instance. Using the deafults for
    # baudrate and port. The desired framerate is 15
    d = Display(16,32,framerate=15)
        
    # Defining a few basic colors    
    red   = Color(255,0,0)
    green = Color(0,255,0)    

    d.fill(green)
    d.setPixel(0,3,red)
    d.setPixel(14,23,red)

    d.update()

Components
----------

The components module contains the :ref:`display-class-doc` class.

Geometry
--------

Dependencies
------------

.. toctree::
   :maxdepth: 2

   display
   geometry
