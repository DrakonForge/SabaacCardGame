"""
Card class that represents a single card in the deck.
"""
class Card:
    # Constant numerical ids for suits
    NO_SUIT = 0
    COINS = 1
    FLASKS = 2
    SABERS = 3
    STAVES = 4
    
    # Returns the name of a suit given its numerical ids
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
    
    # Constructor with an optional name
    def __init__(self, suit, value, name = None):
        self.suit = suit
        self.value = value
        self.name = name
    
    # Returns the name of the card
    def getName(self):
        # If name is defined, return name
        if self.name != None:
            return self.name
        
        # If suit is undefined, cannot generate
        if self.suit == None or self.suit == Card.NO_SUIT:
            return None
        
        # Attempt to generate name based on value
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
    
    # Returns the numerical id of this card's suit
    def getSuitIndex(self):
        return self.suit
    
    # Returns the value of the card
    def getValue(self):
        return self.value
    
    # Allows Card objects to be printed as strings
    def __str__(self):
        return self.getName() + " (" + str(self.getValue()) + ")"

def main():
    max = 15

    for i in range(1, max + 1):
        card = Card(Card.COINS, i)
        print(card)

if __name__ == "__main__":
    main()
