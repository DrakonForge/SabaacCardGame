from card import Card

"""
Player class that represents a player in a Sabaac game.
"""
class Player:
    # Constructor that creates a player with the given name
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.interferenceField = []
        self.chips = 0
    
    # Modifies the player's chips by the given amount
    def changeChips(self, amount):
        self.chips += amount
        
        if self.chips < 0:
            # Shouldn't happen, but just in case:
            print("Error: " + self.name + "'s chips are below 0!")
            self.chips = 0
        
    # Adds a card to the player's hand
    def addToHand(self, card):
        self.hand.append(card)
        
    def addToInterferenceField(self, card):
        self.interferenceField.append(card)
    
    # Clears the player's hand
    def emptyHand(self):
        self.hand = []
    
    def emptyInterferenceField(self):
        self.interferenceField = []
    
    # Returns the player's current hand value
    def calculateHandValue(self):
        handValue = 0
        for card in self.hand:
            handValue += card.getValue()
        for card in self.interferenceField:
            handValue += card.getValue()
        handValue = abs(handValue)
        return handValue
        
    # Prints all cards in the player's hand
    def printHand(self, prefix = ""):
        print("In Hand: ")
        for card in self.hand:
            print(prefix + str(card))
        if len(self.hand) <= 0:
            print("* Empty")
        print()
        print("In Interference Field: ")
        if len(self.interferenceField) <= 0:
            print("* Empty")
        for card in self.interferenceField:
            print(prefix + str(card))
    
    # Returns the card at the given index
    def getCardAtHandIndex(self, index):
        return self.hand[index]
    
    def getCardInInterferenceField(self, index):
        return self.interferenceField[index]
    
    # Removes and returns the card at the given index
    def removeCardAtHandIndex(self, index):
        return self.hand.pop(index)
        
    def removeCardInInterferenceField(self, index):
        return self.interferenceField.pop(index)

    # Returns the player's name
    def getName(self):
        return self.name

    # Returns the player's hand (a list of cards)
    def getHand(self):
        return self.hand
    
    def getInterferenceField(self):
        return self.interferenceField

    # Returns the player's current chips
    def getChips(self):
        return self.chips
        
def main():
    player = Player("Bob")
    player.addToHand(Card(Card.COINS, 1))
    player.addToHand(Card(Card.STAVES, 3))
    player.printHand()
    
if __name__ == "__main__":
    main()
