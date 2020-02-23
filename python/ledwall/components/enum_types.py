from enum import IntEnum

__all__ = ["WireMode"]

class WireMode(IntEnum):
    """
    The wire mode describes the way, the leds are organized on the board. Two ways of wiring are supported.
    *LTR* and *ZIGZAG*. The WireMode class is an Enum. Whenever you have to specifiy a mode, you simply write
    ``WireMode.LTR`` or ``WireMode.ZIGZAG`` 

    **WireMde.LTR  (Left-To-Right)**

    In the mode WireMode.LTR, all rows are going from left to right. The cable for the data line (blue) goes 
    all the way back from the end of one row to the beginning of the next row.

    .. figure:: mode_ltr.png
       :scale: 60 %
       :alt: mode ltr
       :align: center

       WireMode.LTR

    **WireMode.ZIGZAG**

    In the mode WireMode.ZIGZAG all even rows go from left to right where as the the odd rows go from right to left. Organizing leds
    in this way saves a lot of cable for the data line (blue).

    .. figure:: mode_zigzag.png
       :scale: 60 %
       :alt: mode ltr
       :align: center

       WireMode.ZIGZAG

    """

    LTR = 0
    ZIGZAG = 1

