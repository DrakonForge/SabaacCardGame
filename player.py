from card import Card

"""
Player class that represents a player in a Sabaac game.
"""
class Player:
    # Constructor that creates a player with the given name
    def __init__(self, name):
        self.name = name
        self.hand = []
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
    
    # Clears the player's hand
    def emptyHand(self):
        self.hand = []
    
    # Returns the player's current hand value
    def calculateHandValue(self):
        handValue = 0
        for card in self.hand:
            handValue += card.getValue()
        handValue = abs(handValue)
        return handValue
        
    # Prints all cards in the player's hand
    def printHand(self, prefix = ""):
        for card in self.hand:
            print(prefix + str(card))
    
    # Returns the card at the given index
    def getCardAtHandIndex(self, index):
        return self.hand[index]
    
    # Removes and returns the card at the given index
    def removeCardAtHandIndex(self, index):
        return self.hand.pop(index)

    # Returns the player's name
    def getName(self):
        return self.name

    # Returns the player's hand (a list of cards)
    def getHand(self):
        return self.hand

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
