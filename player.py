from card import Card

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.chips = 0
        
    def changeChips(self, amount):
        self.chips += amount
        
    # addToHand(card) -> add a card to hand
    def addToHand(self, card):
        self.hand.append(card)
    
    # emptyHand() -> clears out hand
    def emptyHand(self):
        self.hand = []
        
    def printHand(self):
        for card in self.hand:
            print(card)
    
    # getCardAtHandIndex(index) -> return card at index
    def getCardAtHandIndex(self, index):
        return self.hand[index]
    
    def removeCardAtHandIndex(self, index):
        return self.hand.pop(index)

    def getName(self):
        return self.name

    def getHand(self):
        return self.hand

    def getChips(self):
        return self.chips
        
def main():
    player = Player("Andrew")
    player.addToHand(Card(Card.COINS, 1))
    player.addToHand(Card(Card.STAVES, 3))
    player.printHand()
    
    # print(player.getName())
    # print(player.getChips())
    # print()
    # print(player.getHand())
    # player.addToHand(Card(Card.COINS, 1))
    # print(player.getHand())
    # player.addToHand(Card(Card.STAVES, 3))
    # print(player.getHand())
    # print()
    # print(player.getCardAtHandIndex(1).getName())
    # player.emptyHand()
    # print(player.getHand())
    
if __name__ == "__main__":
    main()
