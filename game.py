from card import Card
from deck import Deck
from player import Player

class Game:
    STARTING_HAND_SIZE = 2
    ANTE = 2
    
    def __init__(self, playerNameList):
        self.deck = Deck.createDeck()
        self.deck.shuffle()
        
        self.playerList = []
        for playerName in playerNameList:
            player = Player(playerName)
            self.playerList.append(player)
            
        self.handPot = 0
    
    def playGame(self):
        while len(self.playerList) > 1:
            self.doRound()
        # Celebrate the last survivor of the apocalypse
    
    def doRound(self):
        self.dealCards()
        self.doBettingPhase(True)
        self.doShiftingPhase()
        self.doDrawingPhase()
        self.doBettingPhase(False)
        self.resolveRound()
        self.confirmPlayAgain()
    
    def dealCards(self):
        for player in self.playerList:
            for i in range(Game.STARTING_HAND_SIZE):
                # deal a card to the player
                nextCard = self.deck.draw()
                player.addToHand(nextCard)
    
    def doBettingPhase(self, withAnte):
        # create a queue of players
        # set min cost
        # while queue is not empty:
            # get player from front of queue
            # display the player's hand
            # prompt player to FOLD, CALL, RAISE, CHECK
            # do weird loop logic help me
            # wiggle our fingers at the hand pot
        pass
    
    def doShiftingPhase(self):
        pass
    
    def doDrawingPhase(self):
        # for each player:
            # display the player's hand
            # choose whether we want to EXCHANGE, DISCARD, or SKIP
            # perform EXCHANGE/DISCARD
        pass
    
    def resolveRound(self):
        # calculate hand values and any combos of each player, determine winner
        # and then give them credits
        pass
    
    def confirmPlayAgain(self):
        # for each player:
            # prompt: Play again? or Quit
            # If Quit, remove them from the list
        pass
    
    # DEAL CARDS
    # BETTING PHASE - FOLD, CALL (MATCH), RAISE (INCREASE), CHECK (IF NO ONE HAS RAISED)
    # - ANTE (BETTING PHASE) - pay (CHECK) or FOLD
    # SHIFTING PHASE
    # DRAWING PHASE - EXCHANGE A CARD, return them to deck (at the bottom), and draw that many to draw OR discard without drawing
    # ANOTHER BETTING ROUND (without ante)
    # RESOLVE
    # PLAY ANOTHER ROUND?
    
    # If everyone folds but one, they win
    # Can leave game if bombing out (credits) or between rounds
    
def main():
    players = [ "Player1", "Player2", "Player3" ]
    game = Game(players)
    
    game.dealCards()
    for player in game.playerList:
        print(player.getName() + "'s Hand:")
        player.printHand()
        print()

if __name__ == "__main__":
    main()
    
    
    
