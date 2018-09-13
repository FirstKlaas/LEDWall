.. display_doc:

ledwall.geometry
================

The geometry module includes some basic shapes that
can be drawn to the display. The basic shapes are
:class:`~ledwall.geometry.Point`, :class:`~ledwall.geometry.Line`,
:class:`~ledwall.geometry.Rectangle`.

Some sample code:

.. code-block:: python

    from ledwall.geometry import *

    p1 = Point(2,4)
    p2 = Point(7,12)

    # Line between two points
    l1 = Line(p1,p2)

    # Line from values (x1,y1,x2,y2)
    l1 = Line.fromTuple((0,0,5,10))

    r1 = Rectangle(2,3,10,20)


Point
-----

.. autoclass:: ledwall.geometry.Point
    :members:

Rectangle
---------

.. autoclass:: ledwall.geometry.Rectangle
    :members:

Line
----

.. autoclass:: ledwall.geometry.Line
    :members:
