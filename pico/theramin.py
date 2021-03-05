# In order for this to work, you'll need a light sensor connected, which wasn't
# in the kit.

from machine import ADC
from common import speaker, button, VOLUME_OFF, VOLUME_OFF, oled_page
import time
import math 

light_sensor = ADC(1)

oled_page(
    "Light theramin",
    "Expose sensor",
    "to more/less",
    "light. Press",
    "button to stop")

speaker.duty_u16(VOLUME_MAX)

print("""
Raise and lower your hands over the light sensor or shine a light on it
(it's between the Pico and the screen.) 
 
To stop, press the black button.
""")

prev = light_sensor.read_u16()

while button.value() == 1:
    light = light_sensor.read_u16()
    print(light)
    if abs(prev - light) > 200: 
        speaker.freq(light // 10)
    prev = light
    time.sleep(0.1)
    
speaker.duty_u16(VOLUME_OFF)