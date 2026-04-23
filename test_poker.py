
from poker import Hand, Poker

if __name__ == "__main__":
    players = [Hand("SB", 100), Hand("BB", 100)]
    game = Poker(players)
    print("All hands:")
    game.getHands()
    print("\nHand for SB:")
    print(game.getHand("SB"))
    print("\nHand for BB:")
    print(game.getHand("BB"))
    print("\nRunning the game:")
    game.runGame()

    print("\nCombined hands:")
    for player in game.players:
        print(f"{player.position}: {[str(card) for card in player.combined]}")
