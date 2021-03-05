Source Code
===========

There was a small bug in MicroPython 1.14 (the version that was the stable
version when I made this project): it was missing the `array` library, which is
required by the driver for the display. Therefore, I installed a 
`beta version of MicroPython 
<https://micropython.org/resources/firmware/rp2-pico-20210305-unstable-v1.14-83-g680ce4532.uf2>`_
as a workaround. This bug will be fixed in v1.15, whenever that comes out.

Starter & Common Stuff
----------------------

Common
++++++

.. literalinclude:: ../pico/common.py
    :language: python
    :caption:

Main (runs on boot)
+++++++++++++++++++

.. literalinclude:: ../pico/main.py
    :language: python
    :caption:

OLED Display Driver
+++++++++++++++++++

*(not authored by Joel)*

.. literalinclude:: ../pico/lib/ssd1306.py
    :language: python
    :caption:

The Sections
------------

Welcome
+++++++

.. literalinclude:: ../pico/welcome.py
    :language: python
    :caption:

Begin
+++++

.. literalinclude:: ../pico/begin.py
    :language: python
    :caption:

Cat
+++

.. literalinclude:: ../pico/cat.py
    :language: python
    :caption:

Connect Four
++++++++++++

.. literalinclude:: ../pico/connectfour.py
    :language: python
    :caption:

Sensors
+++++++

.. literalinclude:: ../pico/sensors.py
    :language: python
    :caption:

Music
+++++

.. literalinclude:: ../pico/music.py
    :language: python
    :caption:

Morse
+++++

.. literalinclude:: ../pico/morse.py
    :language: python
    :caption:

Cryptogram
++++++++++

.. literalinclude:: ../pico/cryptogram.py
    :language: python
    :caption:

Yay
+++

.. literalinclude:: ../pico/yay.py
    :language: python
    :caption:
