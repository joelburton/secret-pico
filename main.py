from common import name, oled_page, oled_wait, speaker, led, led_wait, url
from time import sleep
import uio

speaker.freq(523)
speaker.duty_u16(1500)
sleep(0.15)
speaker.freq(659)
sleep(0.15)
speaker.duty_u16(0)

led.on()

try:
    step = uio.open("/step.txt").read().strip()
except:
    oled_page("CANT READ step")
    step = "welcome"
    sleep(1)

if step == "welcome":
    import welcome
    welcome.start()
    
else:
    oled_page(
        "Welcome back!",
        "Connect using",
        "screen",
        " /dev/tty.usb*")
    led_wait()
    print("""
Welcome back.

You can pick up where you were with:

  >>> import {step}
  >>> {step}.start()
  
(if you know other step names, feel free to use them)
""".format(step=step))

