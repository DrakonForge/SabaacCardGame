class Card:
    NO_SUIT = 0
    COINS = 1
    FLASKS = 2
    SABERS = 3
    STAVES = 4
    
    @staticmethod
    def getSuitName(suit):
        if suit == Card.COINS:
            return "Coins"
        if suit == Card.FLASKS:
            return "Flasks"
        if suit == Card.SABERS:
            return "Sabers"
        if suit == Card.STAVES:
            return "Staves"
        return "None"
    
    # constructor
    def __init__(self, suit, value, name = None):
        self.suit = suit
        self.value = value
        self.name = name
        
    def getName(self):
        # if name is defined, return name
        if self.name != None:
            return self.name
        
        # if suit is undefined, cannot generate
        if self.suit == None:
            return None
        
        # if value is correct, generate name
        if self.value >= 1 and self.value <= 11:
            return str(self.value) + " of " + Card.getSuitName(self.suit)
        
        if self.value == 12:
            return "Commander of " + Card.getSuitName(self.suit)
            
        if self.value == 13:
            return "Mistress of " + Card.getSuitName(self.suit)
        
        if self.value == 14:
            return "Master of " + Card.getSuitName(self.suit)
        
        if self.value == 15:
            return "Ace of " + Card.getSuitName(self.suit)
    
    def getSuitIndex(self):
        return self.suit
    
    def getValue(self):
        return self.value
        
    def __str__(self):
        return self.getName() + " (" + str(self.getValue()) + ")"

def main():
    max = 15

    for i in range(1, max + 1):
        card = Card(Card.COINS, i)
        print(card)

if __name__ == "__main__":
    main()
