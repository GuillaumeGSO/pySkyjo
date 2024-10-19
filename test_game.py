import unittest
from game import Game, Player, Card

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game(2)

    def test_init_game(self):
        self.assertEqual(len(self.game.deck), 150-2*12)
        self.assertEqual(self.game.number_players, 2)
        self.assertEqual(len(self.game.players), 2)

        player0 = self.game.players[0]
        self.assertEqual(len(player0.cards), 12)
        self.assertEqual(player0.name, "Player0")
        self.assertEqual(player0.score, 0)
        
        player1 = self.game.players[1]
        self.assertEqual(len(player1.cards), 12)
        self.assertEqual(player1.name, "Player1")
        self.assertEqual(player1.score, 0)


    def test_round_is_not_over(self):
        # Round is not over (no player has all cards visible)
        player1 = Player("Player 1")
        player1.cards = [Card(0, visible=True), Card(10, visible=False)]
        player2 = Player("Player 2")
        player2.cards = [Card(1,visible=False), Card(-1,visible=True)]
        self.game.players = [player1, player2]
        self.assertIsNone(self.game.get_round_finisher())
        
    
    def test_round_is_over(self):
        # Round is over (one player has all cards visible)
        player1 = Player("Player 1")
        player1.cards = [Card(2,visible=True), Card(7,visible=True)]
        player2 = Player("Player 2")
        player2.cards = [Card(4,visible=False), Card(12,visible=True)]
        self.game.players = [player1, player2]
        
        round_winner = self.game.get_round_finisher()
        self.assertIsInstance(round_winner, Player)
        self.assertEqual("Player 1", round_winner.name)
        
    def test_game_is_not_over(self):
        # Round is over but no player has more than score 100
        player1 = Player("Player 1")
        player1.cards = [Card(0, visible=True), Card(10, visible=True)]
        player1.score = 50
        player2 = Player("Player 2")
        player2.cards = [Card(1,visible=False), Card(-1,visible=True)]
        player2.score = 99
        self.game.players = [player1, player2]
        self.game.update_scores()
        self.assertFalse(self.game.is_game_over())
        self.assertIsNone(self.game.get_game_winner())

    def test_game_over(self):
        # Round is over and one player has more than score 100
        player1 = Player("Player 1")
        player1.cards = [Card(0, visible=True), Card(1, visible=True)]
        player1.score = 80
        player2 = Player("Player 2")
        player2.cards = [Card(2,visible=False), Card(-1,visible=True)]
        player2.score = 99
        self.game.players = [player1, player2]
        self.assertFalse(self.game.is_game_over())
        self.game.update_scores()
        self.assertEqual(81, player1.score)
        self.assertEqual(100, player2.score)
        self.assertTrue(self.game.is_game_over())
        winner = self.game.get_game_winner()
        self.assertIsInstance(winner, Player)
        self.assertEqual("Player 1", winner.name)

    def test_update_scores_round_not_over(self):
        player1 = Player("Player 1")
        player1.cards = [Card(0, visible=True), Card(10, visible=False)]
        player1.score = 10
        player2 = Player("Player 2")
        player2.cards = [Card(2,visible=False), Card(-1,visible=True)]
        player2.score = 20
        self.game.players = [player1, player2]
        self.assertEqual(10, player1.score)
        self.assertEqual(20, player2.score)
        self.game.update_scores()
        self.assertEqual(10, player1.score)
        self.assertEqual(20, player2.score)

    def test_update_scores_round_over_not_game_over(self):
        player1 = Player("Player 1")
        player1.cards = [Card(2, visible=True), Card(4, visible=True)]
        player1.score = 10
        player2 = Player("Player 2")
        player2.cards = [Card(12,visible=False), Card(-2,visible=True)]
        player2.score = 20
        self.game.players = [player1, player2]
        self.assertEqual(10, player1.score)
        self.assertEqual(20, player2.score)
        self.game.update_scores()
        self.assertEqual(16, player1.score)
        self.assertEqual(30, player2.score)

    def test_update_scores_round_over_with_player_malus(self):
        player1 = Player("Player 1")
        player1.cards = [Card(10, visible=True), Card(10, visible=True)]
        player1.score = 10
        player2 = Player("Player 2")
        player2.cards = [Card(12,visible=False), Card(-2,visible=True)]
        player2.score = 50
        self.game.players = [player1, player2]
        self.assertEqual(10, player1.score)
        self.assertEqual(50, player2.score)
        self.game.update_scores()
        self.assertEqual(10+2*(10+10), player1.score)
        self.assertEqual(60, player2.score)

    def test_update_scores_round_over_with_2_player_minimal(self):
        player1 = Player("Player 1")
        player1.cards = [Card(10, visible=True), Card(10, visible=True)]
        player1.score = 10
        player2 = Player("Player 2")
        player2.cards = [Card(12,visible=False), Card(4,visible=True)]
        player2.score = 50
        player3 = Player("Player 3")
        player3.cards = [Card(10,visible=False), Card(10,visible=False)]
        player3.score = 1
        self.game.players = [player1, player2, player3]
        self.assertEqual(10, player1.score)
        self.assertEqual(50, player2.score)
        self.assertEqual(1, player3.score)
        self.game.update_scores()
        self.assertEqual(10+2*(10+10), player1.score)
        self.assertEqual(66, player2.score)
        self.assertEqual(21, player3.score)
        


if __name__ == '__main__':
    unittest.main()