# Sabaac Card Game

## Overview

This program re-creates the [Sabaac](https://starwars.fandom.com/wiki/Sabacc) card game from the *Star Wars* universe, which is essentially "space poker". It was designed as a beginner's project to introduce programming novices to **Python** and **object-oriented programming** concepts. This project was finished in approximately **3 months** by a team of 3, meeting around once per week.

It is played in a **command line**, and all players must use the same machine. It also features a text-based user interface using simple console input/output to play the game.

## How to Run

* If you don't have Python 3.9.0 or greater, install Python [here](https://www.python.org/downloads/). Python 3+ should generally be supported, but it was developed using this version.
* Download the repository and open a command line in the root folder.
* Run `python game.py` to start the game.
  * Enter the number of players to start (minimum 2, maximum 20).
  * Enter the names of each of the players (make sure they are unique!).
  * The game should start!

## Controls

To make choices, input the number corresponding to that choice (shown in parentheses) then press ENTER to submit. The game may also ask you to confirm in certain situations by pressing ENTER.

Since the game must be played on one machine, a whitespace barrier asking the user to switch players appears between each player's action. Press ENTER when the next player is ready to start.

## Sabaac Ruleset

The Sabaac ruleset we used is largely based on [this ruleset](https://www.pagat.com/invented/sabacc.html), though has some differences. A summary of the game and its rules are below.

A Sabaac deck consists of **76 cards**. Each card has a **value** associated with it.

* 4 suits (Coins, Flasks, Sabers, Staves) each consisting of 15 cards:
  * 1 through 11, Commander (12), Mistress (13), Master (14), and Ace (15)
* 2 of each of the following cards:
  * Queen of Air and Darkness (-2)
  * Endurance (-8)
  * Balance (-11)
  * Demise (-13)
  * Moderation (-14)
  * The Evil One (-15)
  * The Star (-17)
  * The Idiot (0)

### Goal

In Sabaac, rounds are played continuously until there are not enough players to continue the game. There is a **Hand Pot**, which is won by winning the round, and a **Sabaac Pot**, which accumulates over time and is won by achieving a **Sabaac**. Players start with 30 chips and must contribute **2 to the Sabaac Pot** and at least **2 to the Hand Pot** each round as an **ante** to continue playing.

In each round, the **goal** is to get a hand value as close to **23** or **-23** as possible, without going over 23 or below -23 (which is known as **bombing out**). At the end of a round, the player with the highest hand (totaling an absolute value of 23 or below) wins the **Hand Pot**.

If a player has a hand total of exactly **23** or **-23**, they achieve a **Pure Sabaac**, and win the **Sabaac Pot** in addition to the Hand Pot. If a player has an **Idiot**, a **2 of any suit**, and a **3 of any suit** (literally read 0-2-3 -> 23), they achieve the **Idiot's Array**, which also wins the **Sabaac Pot** and **beats out Pure Sabaac**.

If two or more players tie for the winning hand, the Hand Pot is sacrificed to the Sabaac Pot, and no player wins either pot for that round (we did not implement Sudden Demise).

### Gameplay Phases

1. **Ante Phase**: All players must pay 2 chips into the Sabaac Pot, or be disqualified.
2. **Deal Phase**: Two cards are dealt to each player.
3. **First Betting Phase**: The minimum bet is set to 2 chips (Hand Pot Ante). Players take actions one after another in a cycle until all players pay the same amount or fold. Players may choose from the following options:
   1. **Fold**: Resign the round without paying any chips.
   2. **Call**: Pay the minimum bet. If they do not have enough to pay the minimum bet, they may choose to **All-in** and pay their remaining chips into the Hand Pot. A player who alls-in is no longer required to pay anything for the rest of the round.
   3. **Raise**: Raise the minimum bet and pay that amount. If this option is chosen, every other player who has not Folded must Call (with the new minimum amount) or Fold.
4. **Draw Phase**: Players take actions one after another in a cycle until all players **Stand** (do nothing). Players may choose from the following options:
   1. **Stand**: Does nothing and passes the action to the next player.
   2. **Draw**: Draws a card from the deck.
   3. **Exchange**: Pick a card from hand to shuffle back into the deck, then draw a card from the deck.
   4. **Insert into IF**: Pick a card from hand to insert into your **Interference Field**, which makes the card **face-up** but **immune to shifting** (discussed later).
   5. **Remove from IF**: Pick a card from your Interference Field to return to your hand.
   6. **Swap from IF**: Pick a card from your Interference Field and a card in hand. Swap them, placing the first card into your hand and the second into the Interference Field.
5. **Second Betting Phase**: Like the first betting round, but the minimum bet is set to 0, allowing players to **Check** (equivalent to Call) if they do not wish to Raise.
6. **Resolution**: All players' hand totals are calculated and a winner (if there is one) is declared, according to the rules described above.
7. **Play Again?**: Each player is given the option to continue playing another round or quit the game. If there is one or fewer players left, the game ends.

### Shifting

Shifting may occur immediately after **either Betting Phase** or after **any player's action in the Draw Phase**. A Shift has a 1/6 chance to occur (the probability of rolling doubles with a pair of six-sided dice).

When a Shift occurs, **all cards in all player's hands are gathered**. Then, those cards are **redistributed** back to the players **randomly**, also ensuring that their hand size is the same as before the shift. For example, if Player A has 2 cards and Player B has 3 cards, they will still have that many cards after the shift, even if the cards themselves are different.

Cards may be placed in the **Interference Field** (IF), which makes them **face-up** (visible to all players) but **immune to shifting**. There is no limit on how many cards may be in the Interference Field, but players can only move cards in and out of the Interference Field **one at a time** (with the exception of **swaps**, which lets you move one card from hand and one card from the Interference Field).

## User Interface

Since this version of the game is played on a command line using the same machine, several features are added to replicate the information given by an actual card game. When it is a player's turn, they have access to the following information:

* An **action log** detailing all previous actions taken by players in the round.
* The current value of the Hand and Sabaac Pot.
* The current state of all other players, including:
  * Whether or not they have folded.
  * How many chips they have.
  * If they are still in the round, their current hand (Using `X` to represent face-down cards, and revealing face-up cards).
* Your current chips, cards in hand, and cards in Interference Field.
