"""Starting point."""

from common import name, oled_page, led, wait, url
from common import speaker, VOLUME_MAX, VOLUME_OFF
from time import sleep
import uio

speaker.freq(1047) # C
speaker.duty_u16(VOLUME_MAX)
sleep(0.15)
speaker.freq(1175) # E
sleep(0.15)
speaker.duty_u16(VOLUME_OFF)

led.on()

try:
    step = uio.open("/step.txt").read().strip()
except:
    step = "welcome"

if step == "welcome":
    # they're just starting, so move for them
    import welcome
    welcome.start()
    
else:
    oled_page(
        "Welcome back!",
        "Connect using",
        "screen",
        " /dev/tty.usb*")
    wait("Press black button")
    print("""
Welcome back.

You can pick up where you were with:

    >>> import {step}
    >>> {step}.start()

(if you know other step names, feel free to use them)
""".format(step=step))
