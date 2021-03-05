from common import rainbow, oled_page, mark

def start():
    mark("begin")
    oled_page("Begin")
    print("""
Yay! You got here!

Of course, that was easy. This time, it will be harder.
You'll need to figure out how to get to the next step.

In the same package as me is a secret closed envelope.
Don't open it; you won't need anything in it until the end.

But outside the box, there was a strange, featureless 
white card. That holds the clue to the next step.

Don't get it wet, or break it, or anything like that.

But see if it responds to something you already own.

To encourage you, here's a few rainbows!
""")
    
    rainbow()
    rainbow()
    rainbow()
    
    print("""
If you ever want to just see a rainbow, you can do:

  >>> from common import rainbow
  >>> rainbow(brightness=0.2, ntimes=1)

p.s. The card may or may not work for you --- reach out
     for help in #secret-pico if you're stuck :)
""")
