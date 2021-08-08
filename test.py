print("Hello, world!")
print("Hello there!")
print("General Kenobi! You are a bold one")

x = 10 + 3

print(x)

kenobi = "bold one"

print("General Kenobi! You are a " + kenobi)

hobbits = [ "frodo", "bilbo", "sam", "merry", "pippin" ]

print()
for hobbit in hobbits:
    print(hobbit)
    
y = 3 + x

if y == 4:
    print("y is 4")
else:
    print("y is not 4")
    print(y)
    
z = y * x
print(z)
z = y / x
print(z)
z = y - x
print(z)
o = 22 / 7
print(o)

dictionary = {
    "h": 3,
    "y": "string is y",
    "x": 1244
}
print(dictionary)
print(dictionary["y"])

def doX():
    global x
    x = x * 1.25
    print(x)
    
doX()
doX()
doX()
doX()
doX()
doX()

class Deck:
    def __init__(self):
        self.numCards = 52

deck = Deck()
print(deck.numCards) # 52
deck.numCards = 1
print(deck.numCards) # 1
deck2 = Deck()
print(deck2.numCards) # 52