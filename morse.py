"""Morse code demonstration."""

from common import button, led, speaker, name, oled
from time import sleep

PACE_SEC = 0.3
PITCH = 600
VOLUME = 1500

# "s" for dit, "l" for dah
LETTER_TO_CODE = {
    ' ': '',
    'a': 'sl',
    'b': 'lsss',
    'c': 'lsls',
    'd': 'lss',
    'e': 's',
    'f': 'ssls',
    'g': 'lls',
    'h': 'ssss',
    'i': 'ss',
    'j': 'slll',
    'k': 'lsl',
    'l': 'slss',
    'm': 'll',
    'n': 'ls',
    'o': 'lll',
    'p': 'slls',
    'q': 'llsl',
    'r': 'sls',
    's': 'sss',
    't': 'l',
    'u': 'ssl',
    'v': 'sssl',
    'w': 'sll',
    'x': 'lssl',
    'y': 'lsll',
    'z': 'llss',
    '1': 'sllll',
    '2': 'sslll',
    '3': 'sssll',
    '4': 'ssssl',
    '5': 'sssss',
    '6': 'lssss',
    '7': 'llsss',
    '8': 'lllss',
    '9': 'lllls',
    '0': 'lllll',
}


speaker.freq(PITCH) 
led.off()

def lookup_code(symbols):
    print(symbols)
    for k, v in LETTER_TO_CODE.items():
        if v == symbols:
            return k
    return "[???]"
    
def play_letter(letter):
    """Play single letter, flashing LED and making sound."""
    
    code = LETTER_TO_CODE.get(letter, None)
    if code is None:
        # space or some other punctuation
        sleep(PACE_SEC * 4)
        return
    
    print(letter, ":", code)
    
    # Draw symbol on display -- first, clear it
    oled.fill_rect(0, 28, 128, 16, 0)
    oled.text(letter.upper(), 0, 29)

    x = 16
    
    for c in code:
        width = 4 if c == 's' else 8
        oled.fill_rect(x, 32, width, 4, 1)
        x += width + 6
        
    oled.show()
    
    # Play symbol
    for c in code:
        pace = PACE_SEC if c == 's' else PACE_SEC * 2
            
        led.high()
        speaker.duty_u16(VOLUME)
        sleep(pace)
        
        led.low()
        speaker.duty_u16(0)
        sleep(PACE_SEC)
        
    sleep(PACE_SEC * 2)
    oled.fill_rect(0, 28, 128, 16, 0)
    
def play(message):
    """Play a message."""
    for c in message.lower():
        play_letter(c)
        
def record():
    """Record and return message."""
    
    print("Start typing your Morse Code message! Wait 5 seconds to exit")

    pressed_time = 0
    delay_time = 0
    symbols = ""
    msg = ""
    x = 0
    
    while True:
        if button.value() == 0:
            # pushed, light LED, play sound, and count how long its pushed
            led.high()            
            speaker.duty_u16(VOLUME)
                
            delay_time = 0
            pressed_time += 1
                
        elif button.value() == 1:
            # not pushed, accumulate symbol/letter/message after appropriate pauses
            speaker.duty_u16(0)
            led.off()

            # if button was just released, capture symbol
            if pressed_time > 0:
                if pressed_time <= 15:
                    symbols += "s"
                    width = 4
                else:
                    symbols += "l"
                    width = 8
                oled.fill_rect(x, 32, width, 4, 1)
                oled.show()
                x += width + 6

            pressed_time = 0
            delay_time += 1

            # break between symbols (find letter)
            if delay_time == 60 and symbols:
                letter = lookup_code(symbols)
                msg += letter
                print(symbols, ":", letter, "=>", msg)
                symbols = ""
                oled.fill_rect(0, 28, 128, 16, 0)
                x = 0    

            # break between words (find word)
            if delay_time == 300: 
                msg += " "
                
            if delay_time == 500:
                print("(Exiting recording mode)")
                oled.fill_rect(x, 28, 128, 16, 0)
                return msg.strip()
            
        sleep(0.01)

def start():
    oled.text("Morse Code", 0, 0)
    oled.show()