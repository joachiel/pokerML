import random

class Card:
    suits = ["♠", "♥", "♦", "♣"]
    def __init__(self, value, suit):
        if not (1 <= value <= 13):
            raise ValueError("Card value must be between 1 and 13")
        self.value = value
        if suit.lower() not in Card.suits:
                raise Exception("Suit must be a valid suit")
        self.suit = suit

    def __str__(self):
        return f"{self.suit}{self.value}"
        
    def printValue(self):
        return f"{self.value}"
        
    def printSuit(self):
        return f"{self.suit}"
        
class Deck():
    def __init__(self):
        self.cards = [Card(j, Card.suits[i]) for i in range(4) for j in range(1, 14)]

    def printDeck(self):
        for card in self.cards:
            print(str(card))

    def getCardTop(self):
        return self.cards.pop()
    
    def shuffle(self):
        random.shuffle(self.cards)

class Hand():
    def __init__(self, position, stack, card1=None, card2=None,):
        self.card1 = card1
        self.card2 = card2
        self.position = position
        self.combined = []
        self.stack = stack

    def setCard1(self, card):
        self.card1 = card

    def setCard2(self, card):
        self.card2 = card

    def getCard1(self):
        return str(self.card1) if self.card1 else None

    def getCard2(self):
        return str(self.card2) if self.card2 else None

    def getCards(self):
        return f"{self.getCard1()}, {self.getCard2()}"
    
    def setCombined(self, cards):
        self.combined = []
        if self.card1:
            self.combined.append(self.card1)
        if self.card2:
            self.combined.append(self.card2)
        self.combined.extend(cards)
        self.combined.sort(key=lambda card: card.value)
    
    def getCombined(self):
        return str(self.combined)
    
    def setStack(self, newStack):
        self.stack = newStack
    
    def getStack(self):
        return self.stack
    
    def betting_round(self, bet):
        if self.stack <= 0:
            return 0.0
        actual_bet = min(self.stack, bet)
        self.stack -= actual_bet
        return actual_bet


class Poker():
    community = []
    positions = ["SB","BB", "UTG", "UTG+1", "UTG+2","LJ","HJ", "CO", "D"]
    def __init__(self, players):
        if not (2 <= len(players) <= 10):
            raise ValueError(f"Number of players must be between 2 and 10, it is {len(players)}")
        self.num_players = len(players)
        self.pot = 0
        self.deck = Deck()
        self.deck.shuffle()
        self.players = players
        for card_num in range(2):
            for player in self.players:
                card = self.deck.getCardTop()
                if card_num == 0:
                    player.setCard1(card)
                else:
                    player.setCard2(card)

    def getHands(self):
        for player in self.players:
            print(f"{player.position}: {player.card1}, {player.card2}")

    def getHand(self, position):
        for player in self.players:
            if player.position == position:
                return (player.getCard1(), player.getCard2())
        return None

    def flop(self):
        self.deck.getCardTop()  # burn card
        self.community = [self.deck.getCardTop() for _ in range(3)]
        print("Flop (community cards):", ', '.join(str(card) for card in self.community))
        return self.community

    def turn(self):
        self.deck.getCardTop()  # burn card
        card = self.deck.getCardTop()
        self.community.append(card)
        print("Turn (community cards):", ', '.join(str(card) for card in self.community))
        return self.community
    
    def river(self):
        self.deck.getCardTop()  # burn card
        card = self.deck.getCardTop()
        self.community.append(card)
        print("river (community cards):", ', '.join(str(card) for card in self.community))
        return self.community
    
    def run_betting_round(self, bet_amount=random.randint(1, 10)):
        """
        Each player bets the given amount (or goes all-in if they have less). Adds all bets to the pot.
        """
        for player in self.players:
            actual_bet = player.betting_round(bet_amount)
            self.pot += actual_bet

    def payout(self, winners):
        if not winners:
            return
        if not isinstance(winners, list):
            winners = [winners]
        share = self.pot / len(winners)
        for player in winners:
            player.stack += share
        self.pot = 0
        
    
    def runGame(self):
        # Pre-flop betting round
        print("\n--- Pre-Flop Betting ---")
        self.run_betting_round()
        print("\n--- Flop ---")
        self.flop()
        print("\n--- Flop Betting ---")
        self.run_betting_round()
        print("\n--- Turn ---")
        self.turn()
        print("\n--- Turn Betting ---")
        self.run_betting_round()
        print("\n--- River ---")
        self.river()
        print("\n--- River Betting ---")
        self.run_betting_round()
        # Set combined hands fo all players after river (community cards complete)
        for player in self.players:
            player.setCombined(self.community)
        