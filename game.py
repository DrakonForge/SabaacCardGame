from card import Card
from deck import Deck
from player import Player

class Game:
    STARTING_HAND_SIZE = 5
    SABAAC_POT_ANTE = 2
    ANTE = 2
    SABAAC_VALUE = 0
    BOMB_OUT = 24
    
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
        self.playerList = []
        self.currentPlayers = []
        for playerName in playerNameList:
            player = Player(playerName)
            player.changeChips(startingChips)
            self.playerList.append(player)
        
        self.deck = None
        self.handPot = 0
        self.sabaacPot = 0
    
    def resetRound(self):
        # Reset current player list
        self.currentPlayers = [ player for player in self.playerList ]
        
        # Empty all hands
        for player in self.playerList:
            player.emptyHand()

        # Reset hand pot
        self.handPot = 0
        
        # Reset deck
        self.deck = Deck.createDeck()
        self.deck.shuffle()
    
    def playGame(self):
        while len(self.playerList) > 1:
            self.doRound()
        # Celebrate the last survivor of the apocalypse
    
    def doRound(self):
        self.doSabaacPhase()
        
        if len(self.playerList) <= 1:
            return
        
        self.resetRound()
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
    
    def doSabaacPhase(self):
        allPlayers = [ player for player in self.playerList ]
        for player in allPlayers:
            if player.getChips() <= Game.SABAAC_POT_ANTE:
                if player.getChips() > 0:
                    print("Sorry,", player.getName() + ". The House always wins :)")
                # You're out
                self.playerList.remove(player)
            else:
                player.changeChips(-Game.SABAAC_POT_ANTE)
                self.sabaacPot += Game.SABAAC_POT_ANTE
            
    def doBettingPhase(self, withAnte):
        if len(self.currentPlayers) <= 1:
            return
        
        print("BETTING PHASE")
        
        # remainingPlayers = copy of self.playerList
        remainingPlayers = [ player for player in self.currentPlayers ]
        minCost = 0
        
        if withAnte:
            minCost = Game.ANTE
            
        totalPaidPerPlayer = {}
        for player in self.currentPlayers:
            totalPaidPerPlayer[player.getName()] = 0
            
        # Skip if there's 1 or less players with the ability to bet
        numWithChips = 0
        for player in self.currentPlayers:
            if player.getChips() > 0:
                numWithChips += 1
        
        if numWithChips <= 1:
            return
        
        # We can assume if chips are 0, they are not out, just broke
        while len(remainingPlayers) > 0:
            # get player from front of queue
            player = remainingPlayers.pop(0)
            
            if player.getChips() <= 0:
                continue
            
            # display the player's hand
            self.printCurrentGameState(player)
            amountNeeded = minCost - totalPaidPerPlayer[player.getName()]
            print("Need to Pay:", amountNeeded)
            
            actions = [ "Fold", "Call" ]
            
            # Cannot both call and check--use the same slot?
            
            if minCost == 0:
                actions[1] = "Check"
            elif amountNeeded >= player.getChips():
                actions[1] = "All-in"
            if amountNeeded < player.getChips():
                actions.append("Raise")
            
            choice = Game.printMenu(actions)
            
            if choice == 1:
                # Fold
                self.currentPlayers.remove(player)
                
                if len(self.currentPlayers) <= 1:
                    return
            if choice == 2:
                if minCost == 0:
                    continue
                
                if amountNeeded > player.getChips():
                    # All-in
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
                playerIndex = self.currentPlayers.index(player)
                
                # [p1, p2, p3, p4]
                remainingPlayers = []
                
                for other in self.currentPlayers[(playerIndex + 1):]:
                    remainingPlayers.append(other)
                
                for other in self.currentPlayers[:playerIndex]:
                    remainingPlayers.append(other)
    
    def doShiftingPhase(self):
        if len(self.currentPlayers) <= 1:
            return
        print("SHIFTING PHASE")
        pass
    
    def doDrawingPhase(self):
        if len(self.currentPlayers) <= 1:
            return
        print("DRAW PHASE")
        for player in self.currentPlayers:
            self.printCurrentGameState(player)
            choice = Game.printMenu(["Draw", "Exchange", "Discard", "Skip"])
            handChanged = False
            
            # TODO: Idiot's Array trumps normal Sabaac
            if choice == 1:
                self.drawCardForPlayer(player)
                handChanged = True
            if choice == 2:
                # exchange
                cardChoice = Game.printMenu(player.getHand())
                discardedCard = player.removeCardAtHandIndex(cardChoice - 1)
                self.drawCardForPlayer(player)
                handChanged = True
                
                self.deck.addCard(discardedCard)
                self.deck.shuffle()
            if choice == 3:
                # discard
                cardChoice = Game.printMenu(player.getHand())
                discardedCard = player.removeCardAtHandIndex(cardChoice - 1)
                pass
            
            player.printHand()
            if handChanged:
                input("Press Enter to continue...")
            
        pass
    
    def resolveRound(self):
        print("RESOLVE PHASE")
        
        maxMagnitude = -1
        winningPlayers = []
        
        for player in self.currentPlayers:
            handValue = 0
            for card in player.getHand():
                handValue += card.getValue()
            handValue = abs(handValue)
            
            if handValue >= Game.BOMB_OUT:
                continue
            
            if handValue == Game.SABAAC_VALUE:
                handValue = 999
            
            if handValue > maxMagnitude:
                maxMagnitude = handValue
                winningPlayers = []
            if handValue >= maxMagnitude:
                winningPlayers.append(player)
        
        if len(winningPlayers) != 1:
            # Tie
            if maxMagnitude == Game.SABAAC_VALUE:
                print("Lmao it's a tie, no one wins")
            else:
                print("It's a tie!", self.handPot, "chips go to the Sabaac pot")
            self.sabaacPot += self.handPot
        else:
            winningPlayer = winningPlayers[0]
            winningPlayer.changeChips(self.handPot)
            
            if maxMagnitude == 999:
                print(winningPlayer.gameName(), "WINS THE SABAAC POT!")
                winningPlayer.changeChips(self.sabaacPot)
                self.sabaacPot = 0
            else:
                print(winningPlayer.getName(), "wins!")
        pass
    
    def confirmPlayAgain(self):
        print("PLAY AGAIN?")
        remainingPlayers = []
        playerCount = len(self.playerList)
        
        for player in self.playerList:
            print(player.getName())
            result = Game.printMenu(["Continue", "Quit"])
            
            if result == 1:
                remainingPlayers.append(player)
            if result == 2:
                playerCount -= 1
                if playerCount == 1:
                    break
                
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
       
    def printCurrentGameState(self, player):
        print(player.getName())
        print("Chips:", player.getChips())
        print("Hand Pot:", self.handPot)
        print("Sabaac Pot:", self.sabaacPot)
        player.printHand()
    
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