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
        self.folded = False
        self.bet_this_round = 0.0

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
    def __init__(self, players, min_raise_multiplier=2.0, blind=2):
        if not (2 <= len(players) <= 10):
            raise ValueError(f"Number of players must be between 2 and 10, it is {len(players)}")
        self.min_raise_multiplier = min_raise_multiplier
        self.blind = blind
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
    
    def post_blinds(self):
        """Post forced small blind (blind/2) and big blind bets before pre-flop."""
        sb, bb = self.players[0], self.players[1]
        sb_amount = self.blind / 2
        bb_amount = float(self.blind)

        sb_actual = sb.betting_round(sb_amount)
        self.pot += sb_actual
        sb.bet_this_round = sb_actual
        print(f"{sb.position} posts small blind: {sb_actual:.2f}")

        bb_actual = bb.betting_round(bb_amount)
        self.pot += bb_actual
        bb.bet_this_round = bb_actual
        print(f"{bb.position} posts big blind: {bb_actual:.2f}")

    def _one_player_left(self):
        return sum(1 for p in self.players if not p.folded) <= 1

    def run_betting_round(self, start_idx=0, current_bet=0.0):
        """
        Each active player chooses to fold, check, call, bet, or raise in turn.
        If a player bets or raises, all other active players must act again.
        Minimum raise is current_bet * min_raise_multiplier (set on the Poker instance).
        start_idx: index of the first player to act (used for pre-flop where UTG acts first).
        current_bet: the bet amount already in play (used when blinds have been posted).
        """
        n = len(self.players)
        queue = [self.players[(start_idx + i) % n] for i in range(n) if not self.players[(start_idx + i) % n].folded]
        if len(queue) <= 1:
            return

        while queue:
            if self._one_player_left():
                return
            player = queue.pop(0)
            if player.folded:
                continue

            to_call = current_bet - player.bet_this_round
            still_active = [p for p in self.players if not p.folded]

            print(f"\n{player.position} | Stack: {player.stack:.2f} | Pot: {self.pot:.2f} | Hand: {player.card1}, {player.card2}", end="")
            print(f" | To call: {to_call:.2f}" if to_call > 0 else "")

            if to_call == 0:
                print("Actions: check (c), bet (b), fold (f)")
                action = input("> ").strip().lower()
                if action in ("f", "fold"):
                    player.folded = True
                elif action in ("b", "bet"):
                    amount = float(input(f"Bet amount (min 1.00, max {player.stack:.2f}): "))
                    amount = max(1.0, min(player.stack, amount))
                    actual = player.betting_round(amount)
                    self.pot += actual
                    player.bet_this_round += actual
                    current_bet = player.bet_this_round
                    for p in still_active:
                        if p is not player and p not in queue:
                            queue.append(p)
                # check: no action needed
            else:
                min_raise_to = current_bet * self.min_raise_multiplier
                print(f"Actions: fold (f), call {to_call:.2f} (c), raise to min {min_raise_to:.2f} (r)")
                action = input("> ").strip().lower()
                if action in ("f", "fold"):
                    player.folded = True
                elif action in ("c", "call"):
                    actual = player.betting_round(to_call)
                    self.pot += actual
                    player.bet_this_round += actual
                elif action in ("r", "raise"):
                    max_raise_to = player.stack + player.bet_this_round
                    amount = float(input(f"Raise to (min {min_raise_to:.2f}, max {max_raise_to:.2f}): "))
                    amount = max(min_raise_to, min(max_raise_to, amount))
                    additional = amount - player.bet_this_round
                    actual = player.betting_round(additional)
                    self.pot += actual
                    player.bet_this_round += actual
                    current_bet = player.bet_this_round
                    for p in still_active:
                        if p is not player and p not in queue:
                            queue.append(p)

    def payout(self, winners):
        if not winners:
            return
        if not isinstance(winners, list):
            winners = [winners]
        share = self.pot / len(winners)
        for player in winners:
            player.stack += share
        self.pot = 0
        
    
    def _reset_street_bets(self):
        for player in self.players:
            player.bet_this_round = 0.0

    def runGame(self):
        # Pre-flop: post blinds then action starts from UTG (index 2)
        print("\n--- Blinds ---")
        self._reset_street_bets()
        self.post_blinds()
        print("\n--- Pre-Flop Betting ---")
        start_idx = 2 if self.num_players > 2 else 0
        self.run_betting_round(start_idx=start_idx, current_bet=float(self.blind))
        if self._one_player_left():
            for player in self.players:
                player.setCombined(self.community)
            return

        print("\n--- Flop ---")
        self.flop()
        print("\n--- Flop Betting ---")
        self._reset_street_bets()
        self.run_betting_round()
        if self._one_player_left():
            for player in self.players:
                player.setCombined(self.community)
            return

        print("\n--- Turn ---")
        self.turn()
        print("\n--- Turn Betting ---")
        self._reset_street_bets()
        self.run_betting_round()
        if self._one_player_left():
            for player in self.players:
                player.setCombined(self.community)
            return

        print("\n--- River ---")
        self.river()
        print("\n--- River Betting ---")
        self._reset_street_bets()
        self.run_betting_round()
        for player in self.players:
            player.setCombined(self.community)
        