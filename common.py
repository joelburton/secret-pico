# common definitions

from machine import Pin, PWM, ADC, I2C
import ssd1306
from time import sleep, sleep_ms
import array
import rp2

name = "Claire"

# Setup OLED display
i2c = I2C(0, scl=Pin(17), sda=Pin(16))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Since this connects to ground, pull it up ---
# the button will be 0 when pushed, 1 when not
button = Pin(11, Pin.IN, Pin.PULL_UP)

# Potentiometer: 0 for far-left, 65535 for far-right
pot = ADC(0)

# LED onboard the Pico (start on so users know we're powered on)
led = Pin(25, Pin.OUT)

# Piezo
speaker = PWM(Pin(15))

def oled_page(title="", s1="", s2="", s3="", s4=""):
    """Show pageful of strings."""
    oled.fill(0)
    oled.text(title, 0, 0)
    oled.text(s1, 0, 16)
    oled.text(s2, 0, 29)
    oled.text(s3, 0, 42)
    oled.text(s4, 0, 55)
    oled.show()


def oled_clear():
    """Clear non-title area."""
    oled.fill_rect(0, 16, 128, 48, 0)
    oled.show()
    

def oled_wait():
    """Wait for button click."""
    # debounce any previous press
    while button.value() == 0:
        pass
    sleep(0.1)
    
    color = 1
    while button.value() == 1:
        oled.fill_rect(122, 58, 6, 6, color)
        oled.show()
        for _ in range(5):
            sleep(0.1)
            if button.value() == 0:
                return
        color = (color + 1) % 2
        
def led_wait():
    """Wait for button click."""
    # debounce prev click
    while button.value() == 0:
        pass
    
    while button.value() == 1:
        led.toggle()
        for _ in range(5):
            sleep(0.1)
            if button.value() == 0:
                return
        print("Press black button")

def url(page):
    return "http://foo.com/" + page

#### NEOPIXEL STUFF

NEOS_COUNT = 1
NEOS_PIN_NUM = 14
NEOS_BRIGHTNESS = 0.2

@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()


def rainbow():
    """Show rainbow on NeoPixel."""
    
    def pixels_show():
        dimmer_ar = array.array("I", [0 for _ in range(NEOS_COUNT)])
        for i,c in enumerate(ar):
            r = int(((c >> 8) & 0xFF) * NEOS_BRIGHTNESS)
            g = int(((c >> 16) & 0xFF) * NEOS_BRIGHTNESS)
            b = int((c & 0xFF) * NEOS_BRIGHTNESS)
            dimmer_ar[i] = (g<<16) + (r<<8) + b
        sm.put(dimmer_ar, 8)
        sleep_ms(10)

    def pixels_set(i, color):
        ar[i] = (color[1]<<16) + (color[0]<<8) + color[2]

    def wheel(pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            return (0, 0, 0)
        if pos < 85:
            return (255 - pos * 3, pos * 3, 0)
        if pos < 170:
            pos -= 85
            return (0, 255 - pos * 3, pos * 3)
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)

    # Create the StateMachine with the ws2812 program, outputting on pin
    sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(NEOS_PIN_NUM))

    # Start the StateMachine, it will wait for data on its FIFO.
    sm.active(1)

    # Display a pattern on the LEDs via an array of LED RGB values.
    ar = array.array("I", [0 for _ in range(NEOS_COUNT)])

    for j in range(255):
        for i in range(NEOS_COUNT):
            rc_index = (i * 256 // NEOS_COUNT) + j
            pixels_set(i, wheel(rc_index & 255))
        pixels_show()
    for i in range(NEOS_COUNT):
        pixels_set(i, (0, 0, 0))
    pixels_show()


