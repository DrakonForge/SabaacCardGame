from card import Card
from deck import Deck
from player import Player

class Game:
    STARTING_HAND_SIZE = 2
    ANTE = 2
    
    @staticmethod
    def printMenu(options):
        index = 1
        for option in options:
            print("(" + str(index) + ") " + str(option))
            index += 1 # index = index + 1
        return Game.getPlayerChoiceFromInput(len(options))
        
    @staticmethod
    # return number within [1, max]
    def getPlayerChoiceFromInput(max):
        while True:
            try:
                result = int(input("Enter a number: "))
            except ValueError:
                print("Must be a number!")
                continue
            
            if result >= 1 and result <= max:
                break
            else:
                print("Must be between 1 and " + str(max) + "!")
            
        return result
        #pass
    
    def __init__(self, playerNameList, startingChips = 30):
        self.deck = Deck.createDeck()
        self.deck.shuffle()
        
        self.playerList = []
        self.foldedPlayers = []
        for playerName in playerNameList:
            player = Player(playerName)
            player.changeChips(startingChips)
            self.playerList.append(player)
            
        self.handPot = 0
    
    def playGame(self):
        while len(self.playerList) > 1:
            self.doRound()
        # Celebrate the last survivor of the apocalypse
    
    def doRound(self):
        self.foldedPlayers = []
        self.handPot = 0
        
        self.dealCards()
        self.doBettingPhase(True)
        self.doShiftingPhase()
        self.doDrawingPhase()
        
        # If someone all-ins in either phase, other players can continue to raise while exempting the other player
        # Second betting phase needs to be skipped entirely if there's an all-in in first phase
        self.doBettingPhase(False)
        self.resolveRound()
        self.confirmPlayAgain()
    
    def dealCards(self):
        for player in self.playerList:
            for i in range(Game.STARTING_HAND_SIZE):
                # deal a card to the player
                self.drawCardForPlayer(player)
    
    def doBettingPhase(self, withAnte):
        print("BETTING PHASE")
        
        # remainingPlayers = copy of self.playerList
        remainingPlayers = [ player for player in self.playerList ]
        minCost = 0
        
        if withAnte:
            minCost = Game.ANTE
            
        totalPaidPerPlayer = {}
        for player in self.playerList:
            totalPaidPerPlayer[player.getName()] = 0
        
        # TODO: Player wins hand if all other players fold
        # TODO: If first player all-ins
        while len(remainingPlayers) > 0:
            # get player from front of queue
            player = remainingPlayers.pop(0)
            
            if player in self.foldedPlayers:
                continue
            
            # display the player's hand
            print(player.getName())
            print("Chips:", player.getChips())
            print("Hand Pot:", self.handPot)
            print("Need to Pay:", minCost - totalPaidPerPlayer[player.getName()])
            player.printHand()
            
            actions = [ "Fold", "Call" ]
            
            # Cannot both call and check--use the same slot?
            
            if minCost == 0:
                actions[1] = "Check"
            if player.getChips() > 1:
                actions.append("Raise")
            
            choice = Game.printMenu(actions)
            
            if choice == 1:
                self.foldedPlayers.append(player)
            if choice == 2:
                if minCost == 0:
                    continue
                
                amountNeeded = minCost - totalPaidPerPlayer[player.getName()]
                
                if amountNeeded > player.getChips():
                    amountNeeded = player.getChips()
                
                player.changeChips(-amountNeeded)
                self.handPot += amountNeeded
                totalPaidPerPlayer[player.getName()] += amountNeeded
            if choice == 3:
                # Disallow this if the player's broke
                print("Input number of chips to raise by.")
                amountToRaise = Game.getPlayerChoiceFromInput(player.getChips() - minCost)
                amountNeeded = amountToRaise + minCost - totalPaidPerPlayer[player.getName()]
                
                player.changeChips(-amountNeeded)
                self.handPot += amountNeeded
                totalPaidPerPlayer[player.getName()] += amountNeeded
                minCost += amountToRaise
                
                # Reset the queue starting with the player afterward
                playerIndex = self.playerList.index(player)
                
                # [p1, p2, p3, p4]
                remainingPlayers = []
                
                for other in self.playerList[(playerIndex + 1):]:
                    if other in self.foldedPlayers:
                        continue
                    remainingPlayers.append(other)
                
                for other in self.playerList[:playerIndex]:
                    if other in self.foldedPlayers:
                        continue
                    remainingPlayers.append(other)
    
    def doShiftingPhase(self):
        print("SHIFTING PHASE")
        pass
    
    def doDrawingPhase(self):
        print("DRAW PHASE")
        for player in self.playerList:
            print(player.getName())
            player.printHand()
            choice = Game.printMenu(["Draw", "Exchange", "Discard", "Skip"])
            
            if choice == 1:
                self.drawCardForPlayer(player)
            if choice == 2:
                # exchange
                cardChoice = Game.printMenu(player.getHand())
                discardedCard = player.removeCardAtHandIndex(cardChoice - 1)
                self.drawCardForPlayer(player)
            if choice == 3:
                # discard
                cardChoice = Game.printMenu(player.getHand())
                discardedCard = player.removeCardAtHandIndex(cardChoice - 1)
                pass
            
            player.printHand()
        pass
    
    def resolveRound(self):
        print("RESOLVE PHASE")
        
        maxMagnitude = -1
        winningPlayer = None
        
        for player in self.playerList:
            handValue = 0
            for card in player.getHand():
                handValue += card.getValue()
            handValue = abs(handValue)
            
            if handValue > maxMagnitude:
                maxMagnitude = handValue
                winningPlayer = player
        
        print(winningPlayer.getName(), "wins!")
        # calculate hand values and any combos of each player, determine winner
        # and then give them credits
        pass
    
    def confirmPlayAgain(self):
        print("PLAY AGAIN?")
        remainingPlayers = []
        
        for player in self.playerList:
            print(player.getName())
            result = Game.printMenu(["Continue", "Quit"])
            
            if result == 1:
                remainingPlayers.append(player)
                
        self.playerList = remainingPlayers
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
    
    def drawCardForPlayer(self, player):
       nextCard = self.deck.draw()
       player.addToHand(nextCard)
    
def main():
    players = [ "Player1", "Player2", "Player3" ]
    game = Game(players)
    game.playGame()
    
    # game.dealCards()
    # for player in game.playerList:
    #     print(player.getName() + "'s Hand:")
    #     player.printHand()
    #     print()
    

if __name__ == "__main__":
    main()
    
    
    
