Sender Classes
==============

Sender classes are responsible for transferring the data from the display to the 
physical device. If a display has no sender, the :meth:`ledwall.components.Display.update` 
method will have no effect. In this case the display serves as a plane framebuffer. 
You can use is to layer several images and manipulate them independently.

Cuurently the library support a serial connection via the :class:`~ledwall.components.SerialSender` 
or a mqtt based communication via the :class:`~ledwall.components.MqttSender`.

Sender
------

.. autoclass:: ledwall.components.Sender
	:members:

SerialSender
------------

.. autoclass:: ledwall.components.SerialSender
	:members:


AsyncSender
-----------

.. autoclass:: ledwall.components.AsyncSender
	:members:	

ConsoleSender
-------------

.. autoclass:: ledwall.components.ConsoleSender
	:members:		

ProgMemSender
-------------

.. autoclass:: ledwall.components.ProgMemSender
	:members:		

ListSender
----------

.. autoclass:: ledwall.components.ListSender
	:members:		
