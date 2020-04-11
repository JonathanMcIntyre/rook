import random

class Game:
    NUMBER_OF_PLAYERS = 4
    NUM_OF_CARDS_IN_KITTY = 5

    def __init__(self):
        self.teams = []
        self.createPlayers()
        self.createDeck()
        self.i_bidTurn = 0
        self.tricks = []
        self.showResults = [False, False, False, False]
        
    def resetDeck(self):
        self.bidAmount = 70
        self.highestBidder = None
        self.trump = "Select"
        self.kitty = []
        self.trick = [None, None, None, None]
        self.state = "bid"
        self.trickWinner = None
        self.colorLed = None
        for player in self.players:
            player["tricks"] = []
            player["bid"] = 70

    def createPlayers(self):
        self.i_playerTurn = 0
        self.players = []
        for i in range(self.NUMBER_OF_PLAYERS):
            self.players.append({
                "number": i+1,
                "name": "Player " + str(i+1),
                "cards": [],
                "bid": 70,
                "points": 0,
                "tricks": [],
            })

    def createDeck(self):
        self.resetDeck()
        deck = []
        colors = ['red', 'yellow', 'black', 'green']
        for color in colors:
            for i in range(1, 15):
                points = 0
                if i == 10 or i == 14:
                    points = 10
                elif i == 5:
                    points = 5
                elif i == 1:
                    points = 15

                rank = i
                if i == 1:
                    rank = 15
                deck.append({
                    "number": i,
                    "color": color,
                    "points": points,
                    "rank": rank
                })
        
        deck.append({
            "number": 0,
            "color": "rook",
            "points": 20,
            "rank": 1,
        })

        random.shuffle(deck)

        for i in range(self.NUM_OF_CARDS_IN_KITTY):
            self.kitty.append(deck.pop())
        
        self.kitty = sorted(self.kitty, key = lambda i: (i["color"], i["rank"])) 

        while len(deck):
            for player in self.players:
                player["cards"].append(deck.pop())

        for player in self.players:
            player["cards"] = sorted(player["cards"], key = lambda i: (i["color"], i["rank"])) 
    
    def bid(self, i_player, bidAmount):
        if bidAmount:
            self.players[i_player]["bid"] = bidAmount
            self.bidAmount = bidAmount
            self.highestBidder = i_player
        else:
            self.players[i_player]["bid"] = 0
        
        if self.isBiddingDone():
            self.tricks = []
            for i in range(self.NUMBER_OF_PLAYERS):
                if self.players[i]["bid"]:
                    self.highestBidder = i
                    self.i_playerTurn = i
                    self.giveKitty(i)
                    self.state = "discard"
                    break
        else:
            self.nextBidder()
        
    def nextTurn(self):
        self.i_playerTurn = self.i_playerTurn + 1
        if self.i_playerTurn == self.NUMBER_OF_PLAYERS:
            self.i_playerTurn = 0

    def nextBidder(self):
        self.nextTurn()
        while self.players[self.i_playerTurn]["bid"] == 0:
            self.nextTurn()
    
    def isBiddingDone(self):
        numberOfBids = 0
        for player in self.players:
            if player["bid"]:
                numberOfBids += 1
        if numberOfBids == 1:
            return True
        return False
    
    def giveKitty(self, i_player):
        self.players[i_player]["cards"].extend(self.kitty)
        self.players[i_player]["cards"] = sorted(self.players[i_player]["cards"], key = lambda i: (i["color"], i["rank"])) 
    
    def removeCardFromHand(self, i_player, discard):
        for i in range(len(self.players[i_player]["cards"])):
            card = self.players[i_player]["cards"][i]
            if card["number"] == discard["number"] and card["color"] == discard["color"]:
                self.players[i_player]["cards"].pop(i)
                break

    def discardCards(self, i_player, discards):
        for discard in discards:
            if discard["number"] == 5 or discard["number"] == 10 or discard["number"] == 14 or discard["number"] == 1 or discard["number"] == 0:
                continue
            self.removeCardFromHand(i_player, discard)
        if len(self.players[i_player]["cards"]) == 13:
            self.state = "choose trump"

    def setTrump(self, color):
        self.trump = color.lower()
        for player in self.players:
            for card in player["cards"]:
                if card["color"] == "rook":
                    card["color"] = self.trump
                    player["cards"] = sorted(player["cards"], key = lambda i: (i["color"], i["rank"]))
                    break 

        self.nextTurn()
        self.state = "play card"

    def playCard(self, i_player, card):
        isRookCard = card["color"] == "rook"
        if card["color"] == "rook":
            card["color"] = self.trump
        if self.trickWinner is None:
            self.trick = [None, None, None, None]
            self.colorLed = card["color"]
            self.trickWinner = i_player
        else:
            if card["color"] != self.colorLed:
                for cardInHand in self.players[i_player]["cards"]:
                    if cardInHand["color"] == self.colorLed:
                        return

            previousWinningCard = self.trick[self.trickWinner]
            if previousWinningCard["color"] != self.trump and card["color"] == self.trump:
                self.trickWinner = i_player
            elif card["color"] == previousWinningCard["color"] and card["rank"] > previousWinningCard["rank"]:
                self.trickWinner = i_player

        self.trick[i_player] = card
        if isRookCard:
            card["color"] = "rook"
        self.removeCardFromHand(i_player, card)

        if (all(playedCard is not None for playedCard in self.trick)):
            self.tricks.append(self.trick)
            self.players[self.trickWinner]["tricks"].append(self.trick)
            self.i_playerTurn = self.trickWinner
            self.trickWinner = None
            if len(self.players[0]["cards"]) == 0:
                self.endRound()
        else:
            self.nextTurn()

    def endRound(self):
        MOST_TRICKS_BONUS = 20
        ALL_TRICKS_BONUS = 100
        team1Points = 0
        team2Points = 0
        for player in [self.players[0], self.players[2]]:
            for trick in player["tricks"]:
                for card in trick:
                    team1Points += card["points"]
        
        for player in [self.players[1], self.players[3]]:
            for trick in player["tricks"]:
                for card in trick:
                    team2Points += card["points"]
        
        if len(self.players[0]["tricks"]) + len(self.players[2]["tricks"]) > len(self.players[1]["tricks"]) + len(self.players[3]["tricks"]):
            team1Points += MOST_TRICKS_BONUS
        elif len(self.players[0]["tricks"]) + len(self.players[2]["tricks"]) < len(self.players[1]["tricks"]) + len(self.players[3]["tricks"]):
            team2Points += MOST_TRICKS_BONUS
        
        if len(self.players[0]["tricks"]) + len(self.players[2]["tricks"]) == 0:
            team2Points += ALL_TRICKS_BONUS
        elif len(self.players[1]["tricks"]) + len(self.players[3]["tricks"]) == 0:
            team1Points += ALL_TRICKS_BONUS

        if team1Points < self.bidAmount and (self.highestBidder == 0 or self.highestBidder == 2):
            self.players[0]["points"] -= self.bidAmount
            self.players[2]["points"] -= self.bidAmount
        else:
            self.players[0]["points"] += team1Points
            self.players[2]["points"] += team1Points

        if team2Points < self.bidAmount and (self.highestBidder == 1 or self.highestBidder == 3):
            self.players[1]["points"] -= self.bidAmount
            self.players[3]["points"] -= self.bidAmount
        else:
            self.players[1]["points"] += team2Points
            self.players[3]["points"] += team2Points
        
        self.i_bidTurn += 1
        if self.i_bidTurn == self.NUMBER_OF_PLAYERS:
            self.i_bidTurn = 0
        self.i_playerTurn = self.i_bidTurn

        self.showResults = [True, True, True, True]

        self.createDeck()


    def getState(self, i_player):
        action = "wait"
        if self.i_playerTurn == i_player:
            action = self.state
        cardsToDiscard = None
        if len(self.players[i_player]["cards"]) > 13:
            cardsToDiscard = len(self.players[i_player]["cards"]) - 13
        
        kitty = []
        if self.state == "discard":
            kitty = self.kitty
        
        tricks = None
        if self.showResults[i_player]:
            self.showResults[i_player] = False
            tricks = self.tricks
        
        i_opponentPlayer = i_player + 1
        if i_opponentPlayer == self.NUMBER_OF_PLAYERS:
            i_opponentPlayer = 0

        return {
            "bidAmount": self.bidAmount,
            "highestBidder": self.highestBidder,
            "playerTurn": self.i_playerTurn,
            "trump": self.trump,
            "playedCards": self.trick,
            "hand": self.players[i_player]["cards"],
            "action": action,
            "cardsToDiscard": cardsToDiscard,
            "kitty": kitty,
            "points": self.players[i_player]["points"],
            "pointsOpponent": self.players[i_opponentPlayer]["points"],
            "tricks": tricks
        }