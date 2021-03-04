from common import oled_page, rainbow

class Cat:
    def __init__(self, name):
        self.name = name
        
    def dance(self, method):
        """Dance the type of dance given."""
        if method.lower() != "tango":
            print(name, " looks a bit puzzled; she normally prefers a different dance.")
        else:
            print("With great enthusiasm", name, "dances a lovely tango with her imaginary partner.")
            print(name, "has something she wants to tell you -- but hasn't told you what the method name")
            print("is. If only there was a way to find that out in Python...")
            
    def inform(self):
        print("""
Great job!

You can learn more about Micropython's 
    
def start():
    oled_page("Python REPL")
   
    """)