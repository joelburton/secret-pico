"""Show to owners when they first boot."""

from common import name, oled_page, wait, wait, url, mark
from time import sleep


def start():
    mark("welcome")
    oled_page(
        "Hi " + name + "!",
        "The cursor at",
        "the bottom right",
        "means 'press the'",
        "black button'")
    wait()

    oled_page(
        "I'm Pico!",
        "I'm so happy to",
        "meet you! Joel",
        "thinks you're",
        "awesome.")
    wait()

    oled_page(
        "Getting Hints",
        "If you get stuck",
        "and need a hint",
        "use Slack",
        "#secret-pico")
    wait()

    oled_page(
        "Let's begin!",
        "Let's move this",
        "convo to your",
        "laptop, ok?")
    wait()

    oled_page(
        "Type in Shell:",
        "screen",
        "  /dev/tty.usb*",
        "",
        "& press RETURN")
    wait()

    oled_page(
        "Connect to me!",
        "",
        "I'll be waiting",
        "for you there :)")
    wait(msg="Press black button")

    oled_page("Serial output")

    print("""
Hi again! It's me, Pico!

I'm a gift wrapped in a puzzle wrapped in an educational
experience. Joel made me just for you and your cohort-mates.

I've got lots to show you, plus a reward at the end. But
first, like any good hero, you have to overcome some challenges.
Don't give up too easily! Part of a challenge is figuring it out.
But, remember, if you get stuck, you ask in #pico-secret.
""")

    input("Press RETURN > ")

    print("""
Along the way, I have some learning material for you. For
example, you should read:

    {url}
""".format(url=url('pico')))

    input("Press RETURN when ready > ")

    print("""
I can be programmed in lots of languages but, of course,
Joel programmed me in Python. It's actually a version of Python
called MicroPython, meant to be run on tiny machines like me.
It has almost all of the normal language features, plus some
of the standard library. We'll be using it throughout.

You'll start each section by importing a Python module,
and then running it's `start()` function. You can always
revisit and earlier section by importing it. Of course, you
won't know all the future sections, so you can't jump ahead :).

Let's begin! I'm going to return you to my Python shell.
When you're ready, you should type:

    >>> import begin
    >>> begin.start()
    
See you there!
""")
