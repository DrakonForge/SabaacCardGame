from card import Card
import random

"""
Deck class that represents a deck of cards.
"""
class Deck:
    # Returns a complete, shuffled deck of Sabaac cards
    @staticmethod
    def createDeck():
        deck = Deck()
        
        # Add suit cards
        # For each suit:
        for suitIndex in range(1, 4 + 1):
            # For each value:
            for cardValue in range(1, 15 + 1):
                # Add card with suit and value
                card = Card(suitIndex, cardValue)
                deck.addCard(card)
        
        # Add face cards
        deck.addFaceCardPair("Queen of Air and Darkness", -2)
        deck.addFaceCardPair("Endurance", -8)
        deck.addFaceCardPair("Balance", -11)
        deck.addFaceCardPair("Demise", -13)
        deck.addFaceCardPair("Moderation", -14)
        deck.addFaceCardPair("The Evil One", -15)
        deck.addFaceCardPair("The Star", -17)
        deck.addFaceCardPair("The Idiot", 0)
        
        # Shuffle the deck
        deck.shuffle()
        
        return deck
        
    # Constructor that creates an empty Deck
    def __init__(self):
        self.deckList = []

    # Adds a card to the bottom of the deck
    def addCard(self, card):
        self.deckList.append(card)
        
    # Adds a pair of identical cards to the bottom of the deck.
    def addFaceCardPair(self, name, value):
        card1 = Card(Card.NO_SUIT, value, name)
        card2 = Card(Card.NO_SUIT, value, name)
        self.addCard(card1)
        self.addCard(card2)
    
    # Shuffles the deck.
    def shuffle(self):
        random.shuffle(self.deckList)

    # Returns and removes the first card from the deck.
    def draw(self):
        if self.getDeckSize() <= 0:
            return None
        return self.deckList.pop(0)
    
    # Prints every card in the deck.
    def printDeck(self):
        for card in self.deckList:
            print(card)
            
    # Returns the list of cards in the deck.
    def getDeckList(self):
        return self.deckList
        
    # Returns the size of the deck.
    def getDeckSize(self):
        return len(self.deckList)
            
def main():
    deck = Deck.createDeck()
    
    print(deck.getDeckSize())
    print(deck.draw())
    print(deck.draw())
    print(deck.draw())
    print()
    print(deck.getDeckSize())
    #deck.printDeck()
    #print(str(len(deck.getDeckList())) + " should be 76")

if __name__ == "__main__":
    main()