from random import shuffle
from string import ascii_uppercase

message = """
Debugging is twice as hard as writing the code in the first place.
Therefore, if you write the code as cleverly as possible, you are,
by definition, not smart enough to debug it.

The most effective debugging tool is still careful thought,
coupled with judiciously placed print statements.

-- Brian Kernighan
"""

alphabet = list(ascii_uppercase)
shuffle(alphabet)
trans = {ascii_uppercase[i]: alphabet[i] for i in range(len(ascii_uppercase))}

for letter in message:
    letter = letter.upper()
    print(trans.get(letter, letter), end="")