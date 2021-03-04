from machine import ADC
from common import speaker
import time

light_sensor = ADC(1)

speaker.duty_u16(1500)

while True:
    light = light_sensor.read_u16()
    print(light)
    speaker.freq(light // 10)
    time.sleep(0.1)
    