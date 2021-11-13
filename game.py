from card import Card
from deck import Deck
from player import Player
import random

"""
Game class that represents a Sabaac game.
"""
class Game:
    STARTING_HAND_SIZE = 2      # The number of cards drawn at the beginning of every round
    SABAAC_POT_ANTE = 2         # The number of chips that must be contributed to the Sabaac pot every round
    HAND_POT_ANTE = 2           # The number of chips that must be contributed to the hand pot every round
    SABAAC_VALUE = 23           # Value needed to achieve Sabaac
    SHIFT_CHANCE = 1.0 / 6.0    # Chance for a Shift to occur with any player action
    
    PURE_SABAAC_VALUE = 999
    IDIOTS_ARRAY_VALUE = 1000
    MAX_PLAYERS = 20
    
    # Prints out a menu of options and returns the player's choice, indexed at 1
    @staticmethod
    def printMenu(title, options, indexOnly=False):
        index = 1
        print()
        print(title)
        for option in options:
            print("(" + str(index) + ") " + str(option))
            index += 1 # index = index + 1
        chosenIndex = Game.getPlayerChoiceFromInput(len(options))
        if indexOnly:
            return chosenIndex
        return options[chosenIndex - 1]
    
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
                
    @staticmethod
    def changePlayerTo(playerName):
        numWhitespace = 50
        for i in range(numWhitespace):
            print()
            
        print("===================================")
        print("= Please change to " + playerName + ".")
        print("===================================")
        print()
        input("Press ENTER to continue...")
            
        for i in range(numWhitespace):
            print()
    
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
        self.actionLog = []
    
    # Resets player hands, hand pot, etc.
    def resetRound(self):
        # Reset current player list
        self.currentPlayers = [ player for player in self.playerList ]
        
        # Empty all hands
        for player in self.playerList:
            player.emptyHand()
            player.emptyInterferenceField()

        # Reset hand pot
        self.handPot = 0
        
        # Reset deck
        self.deck = Deck.createDeck()
        
        # Reset action log
        self.actionLog = []
    
    def playGame(self):
        # While there are two or more players, keep playing
        while len(self.playerList) > 1:
            self.doRound()

        if len(self.playerList) <= 0:
            print("No players remaining, game over!")
        elif len(self.playerList) == 1:
            print(self.playerList[0].getName() + " is the last player remaining, game over!")
    
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
        self.attemptShift()
        self.doDrawingPhase()       # Allow players to draw, exchange, or discard
        self.doBettingPhase(False)  # Second round of betting
        self.attemptShift()
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
                self.actionLog.append(player.getName() + " was kicked from the match.")
            else:
                # Player pays Sabaac pot ante to stay in the game
                player.changeChips(-Game.SABAAC_POT_ANTE)
                self.sabaacPot += Game.SABAAC_POT_ANTE
    
    # Betting phase where players can pay hand pot ante and choose to raise the bet
    def doBettingPhase(self, withAnte):
        # If all but one player has folded, skip this phase
        if len(self.currentPlayers) <= 1:
            return
        
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
            
            Game.changePlayerTo(player.getName())
            
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
            
            choice = Game.printMenu("BETTING PHASE", actions)
            if choice == "Fold":
                self.currentPlayers.remove(player)
                self.actionLog.append(player.getName() + " folded.")
                
                if len(self.currentPlayers) <= 1:
                    return
            if choice == "Call" or choice == "Check" or choice == "All-in":
                if minCost == 0:
                    self.actionLog.append(player.getName() + " checked.")
                    # Check, do nothing
                    continue
                
                if amountNeeded > player.getChips():
                    # Player does not have enough chips, all-in
                    amountNeeded = player.getChips()
                    self.actionLog.append(player.getName() + " WENT ALL IN, entering " + str(amountNeeded) + " into the hand pot.")
                else:
                    self.actionLog.append(player.getName() + " called, entering " + str(amountNeeded) + " into the hand pot.")
                
                # Pay up to the amount needed
                player.changeChips(-amountNeeded)
                self.handPot += amountNeeded
                totalPaidPerPlayer[player.getName()] += amountNeeded
            if choice == "Raise":
                print("Input number of chips to raise by.")
                amountToRaise = Game.getPlayerChoiceFromInput(player.getChips() - minCost)
                
                # Update amountNeeded
                amountNeeded = amountToRaise + minCost - totalPaidPerPlayer[player.getName()]
                
                self.actionLog.append(player.getName() + " raised the hand pot by " + str(amountToRaise) + ", paying a total of " + str(amountNeeded) + ".")
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
    
    # Drawing phase where players can draw, exchange, or discard a card
    def doDrawingPhase(self):
        # If all but one player has folded, skip this phase
        if len(self.currentPlayers) <= 1:
            return
        
        everyoneSkipped = False
        while not everyoneSkipped:
            everyoneSkipped = True
            for player in self.currentPlayers:
                Game.changePlayerTo(player.getName())
                self.printCurrentGameState(player)
                
                menu = ["Stand", "Draw"]
                cardsInHand = len(player.getHand()) > 0
                cardsInIF = len(player.getInterferenceField()) > 0
                
                if cardsInHand:
                    menu.append("Exchange")
                    menu.append("Insert into IF")
                
                if cardsInIF:
                    menu.append("Remove from IF")
                
                if cardsInHand and cardsInIF:
                    menu.append("Swap from IF")
                
                choice = Game.printMenu("DRAW PHASE", menu)
                
                if choice == "Draw":
                    # Draw
                    self.drawCardForPlayer(player)
                    self.actionLog.append(player.getName() + " drew a card.")
                if choice == "Exchange":
                    # Exchange
                    cardChoice = Game.printMenu("Choose a Card From Hand", player.getHand(), indexOnly=True)
                    discardedCard = player.removeCardAtHandIndex(cardChoice - 1)
                    self.drawCardForPlayer(player)
                    # Shuffle the card back into the deck
                    self.deck.addCard(discardedCard)
                    self.deck.shuffle()
                    self.actionLog.append(player.getName() + " exchanged a card.")
                if choice == "Insert into IF":
                    cardChoice = Game.printMenu("Choose Card from Hand", player.getHand(), indexOnly=True)
                    discardedCard = player.removeCardAtHandIndex(cardChoice - 1)
                    player.addToInterferenceField(discardedCard)
                    self.actionLog.append(player.getName() + " put a card into their interference field.")
                if choice == "Remove from IF":
                    cardChoice = Game.printMenu("Choose Card from Interference Field", player.getInterferenceField(), indexOnly=True)
                    discardedCard = player.removeCardInInterferenceField(cardChoice - 1)
                    player.addToHand(discardedCard)
                    self.actionLog.append(player.getName() + " removed a card from their interference field.")
                if choice == "Swap from IF":
                    handChoice = Game.printMenu("Choose Card from Hand", player.getHand(), indexOnly=True)
                    IFChoice = Game.printMenu("Choose Card from Interference Field", player.getInterferenceField(), indexOnly=True)
                    handCard = player.removeCardAtHandIndex(handChoice - 1)
                    IFCard = player.removeCardInInterferenceField(IFChoice - 1)
                    player.addToHand(IFCard)
                    player.addToInterferenceField(handCard)
                    self.actionLog.append(player.getName() + " swapped a card from their interference field.")
                if choice == "Stand":
                    self.actionLog.append(player.getName() + " stood.")
                
                if choice != "Stand":
                    everyoneSkipped = False
                    # Allow player to view their hand again
                    player.printHand()
                    input("Press Enter to continue...")
                self.attemptShift()
    
    # Resolves the round and determines the winner
    def resolveRound(self):
        self.actionLog = []
        maxMagnitude = -1   # Tracks the current maximum magnitude
        winningPlayers = [] # Tracks all players that have value equal to
                            # current maximum magnitude
        
        for player in self.currentPlayers:
            # Calculate hand value
            handValue = player.calculateHandValue()
            
            # If player bombs out, they cannot win
            if handValue > Game.SABAAC_VALUE:
                self.actionLog.append(player.getName() + " bombed out with a hand value of " + str(handValue))
                continue
            
            # If player has a Sabaac, assign them an absurdly high value
            if self.isIdiotsArray(player.getHand(), player.getInterferenceField()):
                # Idiot's Array trumps pure Sabaac
                handValue = Game.IDIOTS_ARRAY_VALUE
                self.actionLog.append(player.getName() + " got an Idiot's Array!")
            elif handValue == Game.SABAAC_VALUE:
                handValue = Game.PURE_SABAAC_VALUE
                self.actionLog.append(player.getName() + " got a Pure Sabaac!")
            else:
                self.actionLog.append(player.getName() + " has a hand value of " + str(handValue))
            
            if handValue > maxMagnitude:
                # New maximum magnitude found, reset the list and update max
                maxMagnitude = handValue
                winningPlayers = []
            if handValue >= maxMagnitude:
                # Add the player as a winner if they have a better or equal hand
                winningPlayers.append(player)
        
        if len(winningPlayers) != 1:
            # It's a tie, hand pot goes to sabaac pot instead
            if maxMagnitude >= Game.PURE_SABAAC_VALUE:
                # Multiple Sabaacs, somehow? Lmao have fun losing
                self.actionLog.append("It's a tie between Sabaac winners, no one wins the sabaac pot")
            else:
                print("It's a tie!")
            self.actionLog.append(self.handPot + " chips are lost to the Sabaac pot")
            self.sabaacPot += self.handPot
        else:
            # Only one winner, award them the hand pot
            winningPlayer = winningPlayers[0]
            winningPlayer.changeChips(self.handPot)
            self.handPot = 0
            
            # If they also got a Sabaac, give them the Sabaac pot too
            if maxMagnitude >= Game.PURE_SABAAC_VALUE:
                self.actionLog.append(winningPlayer.getName() +  " WINS THE SABAAC POT!")
                winningPlayer.changeChips(self.sabaacPot)
                self.sabaacPot = 0
            else:
                self.actionLog.append(winningPlayer.getName() + " wins!")
                
    def isIdiotsArray(self, hand, IF):
        hasIdiot = False
        has2 = False
        has3 = False
        
        for card in hand:
            if card.getValue() == 0:
                hasIdiot = True
            elif card.getValue() == 2:
                has2 = True
            elif card.getValue() == 2:
                has3 = True
                
        for card in IF:
            if card.getValue() == 0:
                hasIdiot = True
            elif card.getValue() == 2:
                has2 = True
            elif card.getValue() == 2:
                has3 = True
        
        return hasIdiot and has2 and has3
    
    # Asks each player if they want to continue
    def confirmPlayAgain(self):
        allPlayers = [player for player in self.playerList]
        
        for player in allPlayers:
            Game.changePlayerTo(player.getName())
            print("===", player.getName() + "'s Turn", "===")
            print("Round Results:")
            for line in self.actionLog:
                print("* " + line)
            result = Game.printMenu("PLAY AGAIN?", ["Yes", "No"])
            
            # Do nothing if they choose to continue
            if result == "No":
                # Player quits
                self.playerList.remove(player)
                
                # If there's only one player left, end early
                if len(self.playerList) <= 1:
                    return
    
    # Has a SHIFT_CHANCE chance to shift
    def attemptShift(self):
        if len(self.currentPlayers) <= 1:
            return
        if random.random() < Game.SHIFT_CHANCE:
            self.shift()
    
    def shift(self):
        cardList = []
        playerHandSizes = {}
        
        # Gather all cards from hands
        for player in self.currentPlayers:
            playerHandSizes[player.getName()] = len(player.getHand())
            for card in player.getHand():
                cardList.append(card)
            player.emptyHand()
            
        random.shuffle(cardList)
        
        # Redistribute
        for player in self.currentPlayers:
            numCards = playerHandSizes[player.getName()]
            for i in range(numCards):
                player.addToHand(cardList.pop(0))
                
        self.actionLog.append("CARDS SHIFTED!")
    
    # Draws a card from the deck and adds it to the player's hand
    def drawCardForPlayer(self, player):
       nextCard = self.deck.draw()
       player.addToHand(nextCard)
    
    # Prints the current state of the game to the player
    def printCurrentGameState(self, player):
        print("===", player.getName() + "'s Turn", "===")
        print("Action Log:")
        for line in self.actionLog:
            print("* " + line)
        print()
        print("Hand Pot:", self.handPot, "| Sabaac Pot:", self.sabaacPot)
        print("Other Players:")
        for otherPlayer in self.playerList:
            if otherPlayer in self.currentPlayers:
                if(player == otherPlayer):
                    continue
                otherPlayerDisplay = "* " + otherPlayer.getName() + " is still in the game. "
                otherPlayerDisplay += "(" + str(otherPlayer.getChips()) + ") "
                otherPlayerDisplay += "("
                
                for card in otherPlayer.getHand():
                    otherPlayerDisplay += "X, "
                if len(otherPlayer.getHand()) > 0:
                    if len(otherPlayer.getInterferenceField()) <= 0:
                        otherPlayerDisplay = otherPlayerDisplay[:-2]
                    
                for card in otherPlayer.getInterferenceField():
                    otherPlayerDisplay += str(card) + ", "
                if len(otherPlayer.getInterferenceField()) > 0:
                    otherPlayerDisplay = otherPlayerDisplay[:-2]
                
                otherPlayerDisplay += ")"
            else:
                otherPlayerDisplay = "* " + otherPlayer.getName() + " has folded. "
                otherPlayerDisplay += "(" + str(otherPlayer.getChips()) + ")"
            print(otherPlayerDisplay)
        print()
        print("Chips:", player.getChips())
        print()
        print("Your Hand (Total = " + str(player.calculateHandValue()) + "):")
        player.printHand("* ")
    
def main():
    numPlayers = int(input("Please enter the number of players: "))
    if numPlayers < 2 or numPlayers > Game.MAX_PLAYERS:
        print("Number not valid, setting to default of 2.");
        numPlayers = 2
    
    players = []
    for i in range(numPlayers):
        players.append(input("Please enter Player " + str(i + 1) + "'s name: "))
    
    game = Game(players)
    game.playGame()
    
if __name__ == "__main__":
    main()
