from card import Card
import random

class Deck:
    # static createDeck() -> return a full Sabaac Deck
    @staticmethod
    def createDeck():
        deck = Deck()
        
        # add suit cards
        # for each suit
        for suitIndex in range(1, 4 + 1):
            # for each value
            for cardValue in range(1, 15 + 1):
                card = Card(suitIndex, cardValue)
                deck.addCard(card)
        
        # add face cards
        deck.addFaceCardPair("Queen of Air and Darkness", -2)
        deck.addFaceCardPair("Endurance", -8)
        deck.addFaceCardPair("Balance", -11)
        deck.addFaceCardPair("Demise", -13)
        deck.addFaceCardPair("Moderation", -14)
        deck.addFaceCardPair("The Evil One", -15)
        deck.addFaceCardPair("The Star", -17)
        deck.addFaceCardPair("The Idiot", 0)
        
        return deck
        
    # constructor
    def __init__(self):
        self.deckList = []

    def addCard(self, card):
        self.deckList.append(card)
        
    # addFaceCardPair(name, value)
    def addFaceCardPair(self, name, value):
        card1 = Card(Card.NO_SUIT, value, name)
        card2 = Card(Card.NO_SUIT, value, name)
        self.addCard(card1)
        self.addCard(card2)
    
    # shuffle() -> shuffle the list
    def shuffle(self):
        random.shuffle(self.deckList)

    # draw() -> return and remove first card from deck
    def draw(self):
        return self.deckList.pop(0)
    
    def printDeck(self):
        for card in self.deckList:
            print(card)
            
    def getDeckList(self):
        return self.deckList
        
    def getDeckSize(self):
        return len(self.deckList)
            
def main():
    deck = Deck.createDeck()
    deck.shuffle()
    
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