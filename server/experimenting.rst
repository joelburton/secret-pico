Experimenting
=============

.. image:: science.jpg
  :width: 19em

You can start with the basics at `Getting Started
<https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/10>`_.
(Skip the part around "add the MicroPython firmware; that's already installed
on your Pico).

**Want to learn more?**

In that bag, I've included some other electronic components you can
use with your Pico:

- Five LEDs, in `red`:red:, `blue`:blue:, `yellow`:gold:, `green`:green:, and `white`:inv-gray:.

  *Quite sensibly, Sterling got five additional clear LEDs, all of which provide
  blue light. I think perhaps they like blue.*

- Five 220Ω ("ohm") *resistors* (the tiny things with long wires sticking out of 
  both ends); the LEDs need something to resist the voltage of the Pico down to 
  the voltage the LEDs want.

- A motion detector (the globe on the green circuit board).

  *Since Winnie was so good-humored about my making her the evil character in our
  security stories, I included a second motion detector for her, so she can be
  alerted if people try to sneak up in different directions.*

- Wires with different kinds of ends (to use them separately, just peel them
  apart).

- A few spare buttons ("*momentary switches*").

.. image:: book.png
  :width: 20em

These things, plus the stuff already on the breadboard, happen to be *exactly*
the components required by the very excellent book
`Get Started with MicroPython on Raspberry Pi Pico
<https://hackspace.raspberrypi.org/books/micropython-pico/pdf/download>`_.
This book walks through some fundamental concepts about programming hardware,
and has several projects using these components.

The artwork makes this book look like it's only for kids, but it has a lot of
useful stuff in it for any programmer.

If you do dive into this book (or just want to play with programming your Pico
in general), you should skip any instructions that have you install MicroPython
with a `.uf2` file --- your Pico already has MicroPython installed. 

.. note:: I included a different display

  In Chapter 10 of this book, they show you how to program a SerLCD 16x2 LCD
  display. I considered using one of those but they're heavy, expensive, use
  a fair amount of power, and are pretty much technology from the 1980s. Instead,
  the display on your Pico is a tiny OLED (organic LED) display. These are a
  very new and interesting technology; they use considerably less power than
  traditional LCD displays and are brighter.

  The model I've included for you is a SSD1306 128x64 OLED display; it uses
  the I2C protocol described in the book, but not the SPI protocol, so you can
  still go through that chapter for the I2C parts.
