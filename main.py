from common import name, oled_page, oled_wait, speaker, led, led_wait, url
from time import sleep

speaker.freq(500)
speaker.duty_u16(1500)
sleep(0.15)
speaker.freq(600)
sleep(0.15)
speaker.duty_u16(0)

led.on()



