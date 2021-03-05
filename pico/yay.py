"""Yay!"""

from common import rainbow, oled_page, joel_msg, mark, url

def start():
    mark("yay")
    oled_page("Yay!")
    rainbow()

    print("""
You did it! It was fun for me to lead you through this.

And here's a personal message from Joel for you:

--

{joel_msg}

--

You can learn more, as well as get the table of contents for everything, along
with permission to dig into that mysterious envelope, at:
    
    {url}

<3 Pico, Joel, and Fluffy
""".format(joel_msg=joel_msg, url=url("yay")))