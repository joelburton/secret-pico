from common import oled_page, rainbow, url, mark

class Cat:
    def __init__(self, name):
        self.name = name
        
    def dance(self, method=None):
        """Dance the type of dance given."""
        if not method:
            print("""
Fluffy looks at you, hoping you'll tell what kind of dance she should do.
""")
            return
        if method.lower() != "tango":
            print("""
{name} looks a bit puzzled; she normally prefers a different dance.
""".format(name=self.name))
        else:
            rainbow()
            print("""
With great enthusiasm, {name}, dances a lovely tango with her imaginary 
partner.

{name} has something she wants to tell you -- but hasn't told you what the
method name is. If only there was a way to find that out in Python...
""".format(name=self.name))
            
    def inform(self):
        print("""
Great job!

You can learn more about Micropython at 

    {url}

When you're ready to move on, go to:

    >>> import connectfour
    >>> connectfour.start()
""".format(url=url("micropython")))

def start():
    mark("cat")
    oled_page("Cat")
    print("""
Of course, since this is all written in Python and you have the REPL, you can
do things like you would in more traditional Python.

For example, I've made a Cat class for you. Go ahead and make an instance of
it (you can substitute any name you'd like):

    >>> fluffy = cat.Cat("Fluffy")

Then, make Fluffy dance!
    """)