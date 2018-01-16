Arduino Mqtt
============

Sketch to receive commands from an mqtt broker. The different commands are coded by defined bytes in the payload of the mqtt message. The skeatch uses the pubsub library.

Init Panel
----------

Initializes the "panel"
If the provided frame number is smaller than the curent frame number,
the operation will be canceled.
If the memory for the leds already has been allocated, the operation 
will be canceled.
If the first byte ist not CMD_SHOW, the operation will be canceled.
 
Byte Position
"""""""""""""

===== ================================================
Index Description
===== ================================================
0     Command Byte. must be CMD_SHOW
1     width of the panel. The number of leds per row.
2     height of the panel. The number of rows.
3     HIGH byte of the initial frame nr. .
4     LOW byte of the initial frame nr. 
===== ================================================

:param cmdbuffer: Pointer the the byte buffer with the command bytes.
:type cmdbuffer: byte*

.. code-block:: python

	void initPanel(byte* cmdbuffer, uint16_t length)

Show Panel
----------
Updates the LEDs.

If the provided frame number is smaller than the curent frame number,
the operation will be canceled. If length is not 3, operation will be canceled.
 
Byte Position
"""""""""""""

===== ================================================
Index Description
===== ================================================
0     Command Byte. must be CMD_SHOW
1     HIGH byte frame nr to be updated.
2     LOW byte frame nr to be updated. 
===== ================================================

.. code-block:: python

	void showPanel(byte* cmdbuffer, uint16_t length)