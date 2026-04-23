import unittest
from types import SimpleNamespace
from poker import Hand, Card
from evaluator import pair


def make_game(players):
    """Helper to create a minimal game object with a players list."""
    return SimpleNamespace(players=players)


def make_player(position, card1, card2, community):
    """Helper to create a Hand with hole cards and community cards already combined."""
    player = Hand(position, 100, card1, card2)
    player.setCombined(community)
    return player


class TestPair(unittest.TestCase):

    def test_higher_pair_wins(self):
        """Player with pair of 7s beats player with pair of 2s."""
        community = [Card(3, "♣"), Card(5, "♦"), Card(9, "♠"), Card(11, "♥"), Card(4, "♣")]
        sb = make_player("SB", Card(7, "♠"), Card(7, "♥"), community)
        bb = make_player("BB", Card(2, "♠"), Card(2, "♥"), community)
        result = pair(make_game([sb, bb]))
        self.assertEqual(result, [sb])

    def test_same_pair_kicker_decides(self):
        """Both have pair of 7s — player with King kicker beats player with 10 kicker."""
        community = [Card(7, "♣"), Card(7, "♦"), Card(9, "♠"), Card(5, "♥"), Card(4, "♣")]
        sb = make_player("SB", Card(13, "♠"), Card(3, "♥"), community)  # kickers: 13, 9, 5
        bb = make_player("BB", Card(10, "♠"), Card(3, "♦"), community)  # kickers: 10, 9, 5
        result = pair(make_game([sb, bb]))
        self.assertEqual(result, [sb])

    def test_no_pair_returns_none(self):
        """Neither player has a pair — pair() should return None."""
        community = [Card(6, "♣"), Card(8, "♦"), Card(10, "♠"), Card(12, "♥"), Card(3, "♣")]
        sb = make_player("SB", Card(2, "♠"), Card(4, "♥"), community)
        bb = make_player("BB", Card(5, "♠"), Card(7, "♥"), community)
        result = pair(make_game([sb, bb]))
        self.assertIsNone(result)

    def test_tied_pair_splits_pot(self):
        """Both players have identical pair and kickers — both should be returned."""
        community = [Card(7, "♣"), Card(7, "♦"), Card(13, "♠"), Card(9, "♥"), Card(5, "♦")]
        sb = make_player("SB", Card(3, "♠"), Card(4, "♥"), community)  # kickers: 13, 9, 5
        bb = make_player("BB", Card(3, "♦"), Card(4, "♣"), community)  # kickers: 13, 9, 5
        result = pair(make_game([sb, bb]))
        self.assertIn(sb, result)  # type: ignore
        self.assertIn(bb, result)  # type: ignore
        self.assertEqual(len(result), 2)  # type: ignore


if __name__ == "__main__":
    unittest.main()
