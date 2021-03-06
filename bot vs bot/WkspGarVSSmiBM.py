"""
workshop garden against smithy big money
"""

import random

class SingleGame:
    def __init__(self):
        self.file = open("game_WkspGarden_SmithyBM.txt", "w")

        self.deck1 = ["treasure-copper", "treasure-copper", "treasure-copper", "treasure-copper", "treasure-copper", "treasure-copper", "treasure-copper", "victory-estate", "victory-estate", "victory-estate"]
        self.deck2 = ["treasure-copper", "treasure-copper", "treasure-copper", "treasure-copper", "treasure-copper", "treasure-copper", "treasure-copper", "victory-estate", "victory-estate", "victory-estate"]

        self.hand1 = []
        self.discard1 = []

        self.hand2 = []
        self.discard2 = []

        self.actions = 0
        self.buys = 0
        self.coins = 0

        self.turnNumber = 0 # turn number actually equals turnNumber / 2 rounded up

        self.duchies = 8
        self.provinces = 8
        
        self.currentPlayer = random.randint(1, 2)

        # player 1
        self.numWorkshop = 0
        self.stopWorkshop = 10
        self.numGarden1 = 0
        self.numEstate1 = 3
        
        self.numSilver1 = 0
        self.turnGold1 = 0

        # player 2
        self.numSmithy = 0
        self.limitSmithy = 2
        self.numSilver2 = 0
        self.limitSilver2 = 20
        self.numProvinces2 = 0
        self.numDuchies2 = 0
        self.numEstate2 = 3
        self.turnGold2 = 0

        self.numCurse2 = 0

    # simulates "inventor" game
    def simulateRun(self):
        self.shuffleDeck(1)
        self.shuffleDeck(2)
        self.draw(5, 1)
        self.draw(5, 2)

        while(self.provinces > 0 and (self.numWorkshop < 10 or self.numGarden1 < 8 or self.numEstate1 < 11)):
            self.turn(self.currentPlayer)
            self.currentPlayer = self.currentPlayer % 2 + 1

        self.file.close()

    # simulates a turn
    def turn(self, player):
        self.turnNumber += 1
        
        self.costReduction = 0
        self.actions = 1
        self.buys = 1
        self.coins = 0

        if(self.currentPlayer == 1):
            self.file.write(str(self.turnNumber) + ": " + str(self.numWorkshop) + ", " + str(self.numGarden1) + ", " + str(self.numEstate1) + "\n") 
            hand = self.hand1
        else:
            self.file.write(str(self.turnNumber) + ": " + str(self.provinces) + ", " + str(self.numSmithy) + ", " + str(self.duchies) + "\n")
            hand = self.hand2
        self.file.write(str(hand) + "\n")

        self.action(player)

        self.file.write(str(hand) + "\n")
        
        self.buy(player)
        self.cleanUp(player)

    # try strategy where buy laboratory if can
    def action(self, player):
        playableActions = []

        if(player == 1):
            hand = self.hand1
            discard = self.discard1
        else:
            hand = self.hand2

        # gets all of the actions in the hand
        for card in hand:
            if(card[:6] == "action"):
                playableActions.append(card)

        # plays the actions
        while(len(playableActions) > 0 and self.actions > 0):
            if("action-workshop" in playableActions):

                self.file.write("play workshop" +"\n")

                if(self.numWorkshop < self.stopWorkshop):
                    self.numWorkshop += 1
                    discard.append("action-workshop")
                elif(self.numGarden1 < 8):
                    self.numGarden1 += 1
                    discard.append("victory-garden")
                elif(self.numWorkshop < 10):
                    self.numWorkshop += 1
                    discard.append("action-workshop")
                elif(self.numEstate1 + self.numEstate2 < 14):
                    self.numEstate1 += 1
                    discard.append("victory-estate")

                self.actions -= 1
                playableActions.remove("action-workshop")
                
            elif("action-smithy" in playableActions):
                for number in range(3):
                    lenBefore = len(hand)
                    
                    self.draw(1, player)
                    card = hand[len(hand) - 1]
                    if(card[:6] == "action" and lenBefore != len(hand)):
                        playableActions.append(card)

                self.actions -= 1
                playableActions.remove("action-smithy")

    # buys stuff based on criteria we decided
    def buy(self, player):
        if(player == 1):
            hand = self.hand1
            discard = self.discard1
        else:
            hand = self.hand2
            discard = self.discard2
        
        # plays all of the treasures that can be played
        for card in hand:
            if(card[:8] == "treasure"):
                if(card[9:] == "copper"):
                    self.coins += 1
                elif (card[9:] == "silver"):
                    self.coins += 2
                else:
                    self.coins += 3

        while(self.buys > 0):
            if(player == 1):
                if(4 <= self.coins):
                    if(self.numWorkshop < self.stopWorkshop):
                        self.numWorkshop += 1
                        discard.append("action-workshop")
                        self.coins -= 3
                    elif(self.numGarden1 < 8):
                        self.numGarden1 += 1
                        discard.append("victory-garden")
                        self.coins -= 4
                    elif(self.numWorkshop < 10):
                        self.numWorkshop += 1
                        discard.append("action-workshop")
                        self.coins -= 3
                    elif(self.numEstate1 + self.numEstate2 < 14):
                        self.numEstate1 += 1
                        discard.append("victory-estate")
                        self.coins -= 2
                elif(3 <= self.coins):
                    if(self.numWorkshop < 10):
                        self.numWorkshop += 1
                        discard.append("action-workshop")
                        self.coins -= 3
                    elif(self.numEstate1 + self.numEstate2 < 14):
                        self.numEstate1 += 1
                        discard.append("victory-estate")
                        self.coins -= 2
                elif(2 <= self.coins):
                    if(self.numEstate1 + self.numEstate2 < 14):
                        self.numEstate1 += 1
                        discard.append("victory-estate")
                        self.coins -= 2
                else:
                    discard.append("treasure-copper")
                    
            else:
                if(8 <= self.coins):
                    discard.append("victory-province")
                    self.coins -= (8)
                    self.provinces -= 1
                    self.numProvinces2 += 1
                if(self.coins >= 6):
                    discard.append("treasure-gold")
                    self.coins -= 6
                    if(self.turnGold2 == 0):
                        self.turnGold2 = self.turnNumber
                elif(self.coins >= 5):
                    if(self.provinces <= 4 and self.duchies > 0):
                        discard.append("victory-duchy")
                        self.duchies -= 1
                        self.coins -= 5
                        self.numDuchies2 += 1
                    else:
                        if(self.numSmithy < self.limitSmithy):
                            discard.append("action-smithy")
                            self.numSmithy += 1
                            self.coins -= 4
                        elif(self.numSilver2 < self.limitSilver2):
                            self.numSilver2 += 1
                            discard.append("treasure-silver")
                            self.coins -= 3
                elif(self.coins >= 4):
                    if(self.numSmithy < self.limitSmithy):
                        discard.append("action-smithy")
                        self.numSmithy += 1
                        self.coins -= 4
                    elif(self.numSilver2 < self.limitSilver2):
                        self.numSilver2 += 1
                        discard.append("treasure-silver")
                        self.coins -= 3
                elif(self.coins >= 3 and self.numSilver2 < self.limitSilver2):
                    self.numSilver2 += 1
                    discard.append("treasure-silver")
                    self.coins -= 3
                
            self.buys -= 1


    # gets rid of cards and ends the turn
    def cleanUp(self, player):
        # since none of the cards are taken out of the hand prior to this,
        # we discard everything during the clean-up phase

        if(player == 1):
            hand = self.hand1
            discard = self.discard1
        else:
            hand = self.hand2
            discard = self.discard2

        numCards = len(hand)
        for card in range(numCards):
            discard.append(hand.pop(0))

        if(player == 1):
            self.draw(5, 1)
        else:
            self.draw(5, 2)
    
    # draws a specified number of cards to the hand
    def draw(self, numCardsWanted, player):

        if(player == 1):
            deck = self.deck1
            hand = self.hand1
        else:    
            deck = self.deck2
            hand = self.hand2
        
        # how many cards have been drawn
        numDrawn = 0
        
        # run this if there are not enough cards in the deck
        if(len(deck) < numCardsWanted):
            # put the cards in the deck right now in the hand
            for card in deck:
                hand.append(card)
            numDrawn += len(hand)

            # shuffle the discard pile and make it the new deck
            if(player == 1):
                self.deck1 = self.discard1.copy()
                self.discard1 = []
                self.shuffleDeck(1)
                deck = self.deck1
                hand = self.hand1
            else:
                self.deck2 = self.discard2.copy()
                self.discard2 = []
                self.shuffleDeck(2)
                deck = self.deck2
                hand = self.hand2
                
        # add cards from the deck until the right number of cards have been drawn
        while(numDrawn < numCardsWanted):
            try:
                hand.append(deck.pop(0))
            except IndexError:
                pass
            numDrawn += 1

    def shuffleDeck(self, player):
        # just shuffles the deck
        if(player == 1):
            random.shuffle(self.deck1)
        else:
            random.shuffle(self.deck2)
            
