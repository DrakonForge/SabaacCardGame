from card import Card
from deck import Deck
from player import Player

"""
Game class that represents a Sabaac game.
"""
class Game:
    STARTING_HAND_SIZE = 5 # The number of cards drawn at the beginning of every round
    SABAAC_POT_ANTE = 2    # The number of chips that must be contributed to the Sabaac pot every round
    HAND_POT_ANTE = 2      # The number of chips that must be contributed to the hand pot every round
    SABAAC_VALUE = 0       # Value needed to achieve Sabaac
    BOMB_OUT = 24          # Bomb-out value where all players with this value or higher lose
    
    # Prints out a menu of options and returns the player's choice, indexed at 1
    @staticmethod
    def printMenu(options):
        index = 1
        for option in options:
            print("(" + str(index) + ") " + str(option))
            index += 1 # index = index + 1
        return Game.getPlayerChoiceFromInput(len(options))
    
    # Prompts the player for a number between [1, max]
    @staticmethod
    def getPlayerChoiceFromInput(max):
        while True:
            try:
                result = int(input("Enter a number: "))
            except ValueError:
                # Did not enter a number, try again
                print("Must be a number!")
                continue
            
            if result >= 1 and result <= max:
                # Number is valid, return the value
                return result
            else:
                # Number was not within right range, try again
                print("Must be between 1 and " + str(max) + "!")
    
    # Constructor that creates a game with the given player list and starting chips
    def __init__(self, playerNameList, startingChips = 30):
        self.playerList = []
        
        # Add players to playerList with startingChips
        for playerName in playerNameList:
            player = Player(playerName)
            player.changeChips(startingChips)
            self.playerList.append(player)
        
        # Placeholder values
        self.currentPlayers = []
        self.deck = None
        self.handPot = 0
        self.sabaacPot = 0
    
    # Resets player hands, hand pot, etc.
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
    
    def playGame(self):
        # While there are two or more players, keep playing
        while len(self.playerList) > 1:
            self.doRound()

        # TODO: Celebrate the last survivor of the apocalypse
    
    # Plays a single round of Sabaac
    def doRound(self):
        self.doSabaacPhase()  # Sabaac pot ante (forced) & eliminating broke players
        
        # Sabaac phase can result in eliminations, so check that the game isn't
        # over before continuing
        if len(self.playerList) <= 1:
            return
        
        self.resetRound()           # Begin the actual round
        self.dealCards()            # Deal cards to everyone
        self.doBettingPhase(True)   # First round of betting, with hand pot ante
        self.doShiftingPhase()      # Random chance to shift
        self.doDrawingPhase()       # Allow players to draw, exchange, or discard
        self.doBettingPhase(False)  # Second round of betting
        self.resolveRound()         # Determine the winner
        self.confirmPlayAgain()     # Allow players to continue or quit
    
    # Deals cards to all players
    def dealCards(self):
        for player in self.playerList:
            for i in range(Game.STARTING_HAND_SIZE):
                # Deal a card to the player
                self.drawCardForPlayer(player)
    
    # Forced Sabaac pot ante; if the player cannot pay this then they
    # are eliminated. This is the only phase where players are eliminated
    # for being broke.
    def doSabaacPhase(self):
        # Create a copy since we are deleting during iteration
        allPlayers = [ player for player in self.playerList ]
        
        for player in allPlayers:
            if player.getChips() <= Game.SABAAC_POT_ANTE:
                # Player is eliminated, remove them from the list
                self.playerList.remove(player)
                if player.getChips() > 0:
                    # Taunt them if they weren't completely broke
                    print("Sorry,", player.getName() + ". The House always wins :)")
            else:
                # Player pays Sabaac pot ante to stay in the game
                player.changeChips(-Game.SABAAC_POT_ANTE)
                self.sabaacPot += Game.SABAAC_POT_ANTE
    
    # Betting phase where players can pay hand pot ante and choose to raise the bet
    def doBettingPhase(self, withAnte):
        # If all but one player has folded, skip this phase
        if len(self.currentPlayers) <= 1:
            return
        
        # TODO: Make these barriers fancier
        print("BETTING PHASE")
        
        # Create a queue of remaining players that need to bet
        # Starts with all players still in the round, so makes a copy
        remainingPlayers = [ player for player in self.currentPlayers ]
        minCost = 0
        
        if withAnte:
            # If it's the first round of betting, the hand pot ante is
            # automatically added. This means it's possible to fold to bow
            # out of the round, avoiding the hand pot ante (but not the Sabaac
            # pot ante).
            minCost = Game.HAND_POT_ANTE
            
        # Create a dictionary of current players and how much they've paid
        # during this betting phase
        totalPaidPerPlayer = {}
        numAbleToBet = 0
        for player in self.currentPlayers:
            if player.getChips() > 0:
                numAbleToBet += 1
            totalPaidPerPlayer[player.getName()] = 0
            
        # Skip if there's 1 or less players with the ability to bet
        # Players with 0 chips are not eliminated, just broke
        if numAbleToBet <= 1:
            return
        
        # Loop until the queue is empty:
        while len(remainingPlayers) > 0:
            # Get player from front of queue
            player = remainingPlayers.pop(0)
            
            # Skip the player if they're broke
            if player.getChips() <= 0:
                continue
            
            amountNeeded = minCost - totalPaidPerPlayer[player.getName()]
            
            # Print the game state + how much the player needs to pay:
            self.printCurrentGameState(player)
            print("Need to Pay:", amountNeeded)
            
            actions = [ "Fold", "Call" ]
            
            if minCost == 0:
                # Turn "Call" into "Check" since there is no cost
                actions[1] = "Check"
            elif amountNeeded >= player.getChips():
                # Turn "Call" into "All-in"
                actions[1] = "All-in"
                
            # If player has more chips than the current amount, allow them
            # to Raise as well
            if amountNeeded < player.getChips():
                actions.append("Raise")
            
            choice = Game.printMenu(actions)
            if choice == 1:
                # Fold
                self.currentPlayers.remove(player)
                
                if len(self.currentPlayers) <= 1:
                    return
            if choice == 2:
                # Call/Check/All-in
                if minCost == 0:
                    # Check, do nothing
                    continue
                
                if amountNeeded > player.getChips():
                    # Player does not have enough chips, all-in
                    amountNeeded = player.getChips()
                
                # Pay up to the amount needed
                player.changeChips(-amountNeeded)
                self.handPot += amountNeeded
                totalPaidPerPlayer[player.getName()] += amountNeeded
            if choice == 3:
                # Raise
                print("Input number of chips to raise by.")
                amountToRaise = Game.getPlayerChoiceFromInput(player.getChips() - minCost)
                
                # Update amountNeeded
                amountNeeded = amountToRaise + minCost - totalPaidPerPlayer[player.getName()]
                
                player.changeChips(-amountNeeded)
                self.handPot += amountNeeded
                totalPaidPerPlayer[player.getName()] += amountNeeded
                minCost += amountToRaise
                
                # Reset the queue starting with the NEXT player
                # All players EXCEPT for the current player must now choose to
                # call or raise again
                playerIndex = self.currentPlayers.index(player)
                
                # Reset the queue
                remainingPlayers = []
                
                # Add all players after the current player
                for other in self.currentPlayers[(playerIndex + 1):]:
                    remainingPlayers.append(other)
                
                # All all players before the current player
                for other in self.currentPlayers[:playerIndex]:
                    remainingPlayers.append(other)
    
    # Shifting phase
    def doShiftingPhase(self):
        # If all but one player has folded, skip this phase
        if len(self.currentPlayers) <= 1:
            return
        
        print("SHIFTING PHASE")
        # TODO: Still don't know what this phase does tbh
    
    # Drawing phase where players can draw, exchange, or discard a card
    def doDrawingPhase(self):
        # If all but one player has folded, skip this phase
        if len(self.currentPlayers) <= 1:
            return
        
        print("DRAW PHASE")
        for player in self.currentPlayers:
            self.printCurrentGameState(player)
            choice = Game.printMenu(["Draw", "Exchange", "Discard", "Skip"])
            handChanged = False
            
            if choice == 1:
                # Draw
                self.drawCardForPlayer(player)
                handChanged = True
            if choice == 2:
                # Exchange
                cardChoice = Game.printMenu(player.getHand())
                discardedCard = player.removeCardAtHandIndex(cardChoice - 1)
                self.drawCardForPlayer(player)
                handChanged = True
                
                # Shuffle the card back into the deck
                self.deck.addCard(discardedCard)
                self.deck.shuffle()
            if choice == 3:
                # Discard
                cardChoice = Game.printMenu(player.getHand())
                discardedCard = player.removeCardAtHandIndex(cardChoice - 1)
                pass
            
            if handChanged:
                # Allow player to view their hand again
                player.printHand()
                input("Press Enter to continue...")
    
    # Resolves the round and determines the winner
    def resolveRound(self):
        print("RESOLVE PHASE")
        
        SABAAC_BONUS = 999
        
        maxMagnitude = -1   # Tracks the current maximum magnitude
        winningPlayers = [] # Tracks all players that have value equal to
                            # current maximum magnitude
        
        for player in self.currentPlayers:
            # Calculate hand value
            handValue = player.calculateHandValue()
            
            # If player bombs out, they cannot win
            if handValue >= Game.BOMB_OUT:
                continue
            
            # TODO: Idiot's Array trumps normal Sabaac
            # If player has a Sabaac, assign them an absurdly high value
            if handValue == Game.SABAAC_VALUE:
                handValue = SABAAC_BONUS
            
            if handValue > maxMagnitude:
                # New maximum magnitude found, reset the list and update max
                maxMagnitude = handValue
                winningPlayers = []
            if handValue >= maxMagnitude:
                # Add the player as a winner if they have a better or equal hand
                winningPlayers.append(player)
        
        if len(winningPlayers) != 1:
            # It's a tie, hand pot goes to sabaac pot instead
            if maxMagnitude == SABAAC_BONUS:
                # Multiple Sabaacs, somehow? Lmao have fun losing
                print("Lmao it's a tie, no one wins")
            else:
                print("It's a tie!", self.handPot, "chips go to the Sabaac pot")
            self.sabaacPot += self.handPot
        else:
            # Only one winner, award them the hand pot
            winningPlayer = winningPlayers[0]
            winningPlayer.changeChips(self.handPot)
            self.handPot = 0
            
            # If they also got a Sabaac, give them the Sabaac pot too
            if maxMagnitude == SABAAC_BONUS:
                print(winningPlayer.gameName(), "WINS THE SABAAC POT!")
                winningPlayer.changeChips(self.sabaacPot)
                self.sabaacPot = 0
            else:
                print(winningPlayer.getName(), "wins!")
    
    # Asks each player if they want to continue
    def confirmPlayAgain(self):
        print("PLAY AGAIN?")
        allPlayers = [player for player in self.playerList]
        
        for player in allPlayers:
            self.printCurrentGameState(player)
            result = Game.printMenu(["Continue", "Quit"])
            
            # Do nothing if they choose to continue
            if result == 2:
                # Player quits
                self.playerList.remove(player)
                
                # If there's only one player left, end early
                if len(self.playerList) <= 1:
                    return
    
    # Draws a card from the deck and adds it to the player's hand
    def drawCardForPlayer(self, player):
       nextCard = self.deck.draw()
       player.addToHand(nextCard)
    
    # Prints the current state of the game to the player
    def printCurrentGameState(self, player):
        print("===", player.getName() + "'s Turn", "===")
        print("Hand Pot:", self.handPot, "| Sabaac Pot:", self.sabaacPot)
        print("Other Players:")
        for player in self.playerList:
            # TODO: Print their hand size, number of chips, and if they've folded
            # Ex. "* Player2 is still in the game. (3 cards in hand, 5 chips)"
            # or  "* Player3 has folded. (5 chips)"
            # or something fancier, idk
            pass
        print()
        print("Chips:", player.getChips())
        print("Your Hand (Total = " + str(player.calculateHandValue()) + "):")
        player.printHand("* ")
    
def main():
    players = [ "Player1", "Player2", "Player3" ]
    game = Game(players)
    game.playGame()
    
if __name__ == "__main__":
    main()
