from common import oled_page, url, mark
import machine

def start():
    mark("sensors")
    # Convert a 16-bit number to 0 - 3.3 (Pico runs at 3.3volt)
    CONVERSION_FACTOR = 3.3 / 65535

    # Define the ADC pin number for the thermistor
    temperature_sensor = machine.ADC(4)

    # read voltage from temp sensor and convert into volts (0 - 3.3V)
    reading = temperature_sensor.read_u16() * CONVERSION_FACTOR

    # convert that to the actual temperature in Celsius:
    # 0.706V is 27 degrees C, with a slope of -1.721mV per degree.
    temperature = 27 - (reading - 0.706) / 0.001721

    oled_page("Sensors", "{temperature}C".format(temperature=temperature))
    print("""
Want to know a fun fact?

It's about {temperature} degrees Celsius where you are.

I can tell the approximate temperature from a sensor built in to me. In fact,
reading sensors is something I'm awesome at.

You can learn more at:

    {url}

When you'd like to move on:

    >>> import music
    >>> music.start()
""".format(url=url("sensors"), temperature=temperature))
