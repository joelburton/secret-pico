from common import oled_page, rainbow, url, mark

def start():
    mark("cryptogram")
    oled_page("Cryptogram")
    print("""
An important message arrived just a moment ago, but I can't seem
to puzzle out what it means:


MXCLAAPKA PB UJPYX QB VQOM QB JOPUPKA UVX YFMX PK UVX SPOBU EDQYX.
UVXOXSFOX, PS RFL JOPUX UVX YFMX QB YDXZXODR QB EFBBPCDX, RFL QOX,
CR MXSPKPUPFK, KFU BWQOU XKFLAV UF MXCLA PU.

UVX WFBU XSSXYUPZX MXCLAAPKA UFFD PB BUPDD YQOXSLD UVFLAVU,
YFLEDXM JPUV ILMPYPFLBDR EDQYXM EOPKU BUQUXWXKUB.

-- COPQK NXOKPAVQK


A friendly secret agent told me that it's enciphered using a
"monoalphabetic substitution cipher" (each letter in the message
corresponds in a 1-to-1 relationship with another letter.)

These kind of codes, often called "cryptograms", can be a fun
puzzle to solve. You can find some ideas about how to approach
one from the notes from my Cryptography lecture or at:

  https://www.simonsingh.net/The_Black_Chamber/crackingsubstitution.html
  
When you've broken the code, you can answer a question about the
quotation, and I'll tell you where to find the final step.
""")
    
    while True:
        subject = input("In one word, what is the subject of this quote? > ")
        if subject.lower() == "debugging":
            break
        print("\nNope.\n")
        
    rainbow()
    print("""
Great job! 

Read about this: 

    {url}

Proceed to the next step with:

  >> import yay
  yay.start()
""".format(url=url("decipher")))