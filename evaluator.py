from poker import Poker, Hand, Deck
def royalflush(game):
    royal_values = {10, 11, 12, 13, 1}
    for player in game.players:
        # Group cards by suit
        suit_groups = {}
        for card in player.combined:
            suit_groups.setdefault(card.suit, set()).add(card.value)
        # Check each suit for royal flush
        for suit, values in suit_groups.items():
            if royal_values.issubset(values):
                return player
    return None

def straightflush(game):
    best_players = []
    best_high = None
    for player in game.players:
        # Group cards by suit
        suit_groups = {}
        for card in player.combined:
            suit_groups.setdefault(card.suit, []).append(card.value)
        # Check each suit for straight flush
        for suit, values in suit_groups.items():
            vals = sorted(set(values))
            # Handle Ace as both high (14) and low (1)
            if 1 in vals:
                vals.append(14)
            for i in range(len(vals) - 4):
                window = vals[i:i+5]
                if all(window[j] - window[j-1] == 1 for j in range(1, 5)):
                    high = window[-1]
                    if best_high is None or high > best_high:
                        best_high = high
                        best_players = [player]
                    elif high == best_high:
                        best_players.append(player)
    if best_players:
        return best_players
    return None

def fourofakind(game):
    best_players = []
    best_value = None
    for player in game.players:
        value_counts = {}
        for card in player.combined:
            value_counts[card.value] = value_counts.get(card.value, 0) + 1
        for value, count in value_counts.items():
            if count == 4:
                if best_value is None or value > best_value:
                    best_value = value
                    best_players = [player]
                elif value == best_value:
                    best_players.append(player)
    if best_players:
        return best_players
    return None

def fullhouse(game):
    best_players = []
    best_three = None
    best_pair = None
    for player in game.players:
        value_counts = {}
        for card in player.combined:
            value_counts[card.value] = value_counts.get(card.value, 0) + 1
        threes = sorted([v for v, c in value_counts.items() if c >= 3], reverse=True)
        pairs = sorted([v for v, c in value_counts.items() if c >= 2 and v not in threes], reverse=True)
        if threes and pairs:
            three_val = threes[0]
            pair_val = pairs[0]
            if best_three is None or three_val > best_three:
                best_three = three_val
                best_pair = pair_val
                best_players = [player]
            elif three_val == best_three:
                if best_pair is None or pair_val > best_pair:
                    best_pair = pair_val
                    best_players = [player]
                elif pair_val == best_pair:
                    best_players.append(player)
    if best_players:
        return best_players
    return None

def flush(game):
    best_players = []
    best_high = None
    for player in game.players:
        suit_groups = {}
        for card in player.combined:
            suit_groups.setdefault(card.suit, []).append(card.value)
        for suit, values in suit_groups.items():
            if len(values) >= 5:
                top_five = sorted(values, reverse=True)[:5]
                high = top_five[0]
                if best_high is None or high > best_high:
                    best_high = high
                    best_players = [player]
                elif high == best_high:
                    best_players.append(player)
    if best_players:
        return best_players
    return None

def straight(game):
    best_players = []
    best_high = None
    for player in game.players:
        values = sorted(set(card.value for card in player.combined))
        # Handle Ace as both high (14) and low (1)
        if 1 in values:
            values.append(14)
        for i in range(len(values) - 4):
            window = values[i:i+5]
            if all(window[j] - window[j-1] == 1 for j in range(1, 5)):
                high = window[-1]
                if best_high is None or high > best_high:
                    best_high = high
                    best_players = [player]
                elif high == best_high:
                    best_players.append(player)
    if best_players:
        return best_players
    return None

def threeofakind(game):
    best_players = []
    best_value = None
    best_kickers = None
    for player in game.players:
        value_counts = {}
        for card in player.combined:
            value_counts[card.value] = value_counts.get(card.value, 0) + 1
        three_val = None
        for value, count in value_counts.items():
            if count == 3:
                if three_val is None or value > three_val:
                    three_val = value
        if three_val is not None:
            # Get all kicker values (not part of the three of a kind)
            kickers = sorted([v for v in value_counts.keys() if v != three_val], reverse=True)
            # Only consider the top two kickers
            kicker_tuple = tuple(kickers[:2])
            if best_value is None or three_val > best_value:
                best_value = three_val
                best_kickers = kicker_tuple
                best_players = [player]
            elif three_val == best_value:
                if kicker_tuple > best_kickers:
                    best_kickers = kicker_tuple
                    best_players = [player]
                elif kicker_tuple == best_kickers:
                    best_players.append(player)
    if best_players:
        return best_players
    return None

def twopair(game):
    best_players = []
    best_pairs = None
    best_kicker = None
    for player in game.players:
        value_counts = {}
        for card in player.combined:
            value_counts[card.value] = value_counts.get(card.value, 0) + 1
        pairs = sorted([v for v, c in value_counts.items() if c >= 2], reverse=True)
        if len(pairs) >= 2:
            top_two = tuple(pairs[:2])
            # Find the highest kicker not in the pairs
            kicker = max([v for v in value_counts if v not in top_two], default=-1)
            if best_pairs is None or top_two > best_pairs:
                best_pairs = top_two
                best_kicker = kicker
                best_players = [player]
            elif top_two == best_pairs:
                if kicker > best_kicker:
                    best_kicker = kicker
                    best_players = [player]
                elif kicker == best_kicker:
                    best_players.append(player)
    if best_players:
        return best_players
    return None

def pair(game):
    for player in game.players:
        value_counts = {}
        for card in player.combined:
            value_counts[card.value] = value_counts.get(card.value, 0) + 1
        if any(count == 2 for count in value_counts.values()):
            return player
    return None

def highcard(game):
    best_players = []
    best_cards = None
    for player in game.players:
        # Get the 5 highest cards
        top_five = sorted([card.value for card in player.combined], reverse=True)[:5]
        top_five_tuple = tuple(top_five)
        if best_cards is None or top_five_tuple > best_cards:
            best_cards = top_five_tuple
            best_players = [player]
        elif top_five_tuple == best_cards:
            best_players.append(player)
    if best_players:
        return best_players
    return None

def evaluate_winner(game):
    # List of (function, hand name) in order of poker hand strength
    hand_checks = [
        (royalflush, "Royal Flush"),
        (straightflush, "Straight Flush"),
        (fourofakind, "Four of a Kind"),
        (fullhouse, "Full House"),
        (flush, "Flush"),
        (straight, "Straight"),
        (threeofakind, "Three of a Kind"),
        (twopair, "Two Pair"),
        (pair, "Pair"),
        (highcard, "High Card")
    ]
    for func, name in hand_checks:
        result = func(game)
        if result:
            if isinstance(result, list):
                print(f"Winner(s) with {name}: {[p.position for p in result]}")
            else:
                print(f"Winner with {name}: {result.position}")
            game.payout(result)
            return result
    print("No winner found.")
    return None


# Run 5 games and print stacks at the end
num_players = 4

if __name__ == "__main__":
    num_players = 4
    positions = ["SB","BB", "UTG", "UTG+1", "UTG+2","LJ","HJ", "CO", "D"]
    players = [Hand(positions[i], 100.00) for i in range(num_players)]
    for i in range(10):
        print(f"\n=== Game {i+1} ===")
        game = Poker(players)
        # Print each player's hand (hole cards)
        print("Player hands:")
        for player in players:
            print(f"{player.position}: {player.card1}, {player.card2}")
        game.runGame()
        evaluate_winner(game)
        print("Stacks after game:")
        for player in players:
            print(f"{player.position}: {player.stack}")
        # Reset deck, community, and pot for next game
        game.deck = Deck()
        game.deck.shuffle()
        game.community = []
        game.pot = 0
        for player in game.players:
            player.card1 = None
            player.card2 = None
            player.combined = []

    print("\nFinal stacks:")
    total = 0
    for player in players:
        print(f"{player.position}: {player.stack}")
        total += player.stack
    print(f"Total chips in play: {total}")


# Individualize betting to each player
# Make the bet be an input
# Also add side pots, you can only win what you bet, if some one bets more it gets in a side pot