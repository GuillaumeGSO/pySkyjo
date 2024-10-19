import unittest
from game import Game, Player, Card

class TestGame(unittest.TestCase):
    def setUp(self):
        #self.game = Game(2)
        pass

    def test_generate_players_simple(self):
        game = Game(4)
        game.players = []
        players = game.generate_players()
        self.assertEqual(len(players), 4)
    
    def test_generate_players_zero(self):
        game = Game(0)
        game.players = []
        players = game.generate_players()
        #should error
        self.assertEqual(len(players), 0)
    
    def test_generate_players_wrong(self):
        game = Game(-1)
        players = game.generate_players()
        #should error
        self.assertEqual(len(players), 0)

    def test_reorder_players_first_is_first(self):
        game = Game(4)
        self.assertEqual(len(game.players), 4)
        players=game.reorder_players(game.players[0])
        self.assertEqual(players[0].id, 0)
        self.assertEqual(players[1].id, 1)
        self.assertEqual(players[2].id, 2)
        self.assertEqual(players[3].id, 3)

    def test_reorder_players_first_is_second(self):
        game = Game(4)
        players = game.reorder_players(game.players[1])
        self.assertEqual(players[0].id, 1)
        self.assertEqual(players[1].id, 2)
        self.assertEqual(players[2].id, 3)
        self.assertEqual(players[3].id, 0)

    def test_reorder_players_first_is_third(self):
        game = Game(4)
        players=game.reorder_players(game.players[2])
        self.assertEqual(players[0].id, 2)
        self.assertEqual(players[1].id, 3)
        self.assertEqual(players[2].id, 0)
        self.assertEqual(players[3].id, 1)

    def test_reorder_players_first_is_fourth(self):
        game = Game(4)
        players=game.reorder_players(game.players[3])
        self.assertEqual(players[0].id, 3)
        self.assertEqual(players[1].id, 0)
        self.assertEqual(players[2].id, 1)
        self.assertEqual(players[3].id, 2)

    def test_generate_deck(self):
        game = Game(2)
        self.assertEqual(len(game.deck), 0)
        deck = game.generate_deck()
        self.assertEqual(len(deck), 150)
        self.assertEqual(len([card for card in deck if card.value == -2]),10)
        self.assertEqual(len([card for card in deck if card.value == -1]),10)
        self.assertEqual(len([card for card in deck if card.value == 0]),10)
        self.assertEqual(len([card for card in deck if card.value == 1]),10)
        self.assertEqual(len([card for card in deck if card.value == 2]),10)
        self.assertEqual(len([card for card in deck if card.value == 3]),10)
        self.assertEqual(len([card for card in deck if card.value == 4]),10)
        self.assertEqual(len([card for card in deck if card.value == 5]),10)
        self.assertEqual(len([card for card in deck if card.value == 6]),10)
        self.assertEqual(len([card for card in deck if card.value == 7]),10)
        self.assertEqual(len([card for card in deck if card.value == 8]),10)
        self.assertEqual(len([card for card in deck if card.value == 9]),10)
        self.assertEqual(len([card for card in deck if card.value == 10]),10)
        self.assertEqual(len([card for card in deck if card.value == 11]),10)
        self.assertEqual(len([card for card in deck if card.value == 12]),10)
        self.assertEqual(len([card for card in deck if card.value == 13]),0)

    def test_init_game(self):
        game= Game(2)
        game.init_game()
        self.assertEqual(game.number_players, 2)
        self.assertEqual(len(game.players), 2)

        player0 = game.players[0]
        self.assertEqual(player0.id, 0)
        self.assertEqual(player0.score, 0)
        
        player1 = game.players[1]
        self.assertEqual(player1.id,1)
        self.assertEqual(player1.score, 0)

    def test_init_round(self):
        game = Game(2)
        self.assertEqual(len(game.deck), 0)
        game.init_round()
        #deckLength - nbPlayer*12 - visibleStartingCar
        self.assertEqual(len(game.deck), 150-(12*2)-1)


    def test_round_is_not_over(self):
        game= Game(2)
        # Round is not over (no player has all cards visible)
        player1 = Player(1)
        player1.cards = [Card(0, visible=True), Card(10, visible=False)]
        player2 = Player(2)
        player2.cards = [Card(1,visible=False), Card(-1,visible=True)]
        game.players = [player1, player2]
        self.assertIsNone(game.get_round_finisher())
        
    
    def test_round_is_over(self):
        game= Game(2)
        # Round is over (one player has all cards visible)
        player1 = Player(1)
        player1.cards = [Card(2,visible=True), Card(7,visible=True)]
        player2 = Player(2)
        player2.cards = [Card(4,visible=False), Card(12,visible=True)]
        game.players = [player1, player2]
        
        round_winner = game.get_round_finisher()
        self.assertIsInstance(round_winner, Player)
        self.assertEqual(1, round_winner.id)
        
    def test_game_is_not_over(self):
        game= Game(2)
        # Round is over but no player has more than score 100
        player1 = Player(1)
        player1.cards = [Card(0, visible=True), Card(10, visible=True)]
        player1.score = 50
        player2 = Player(2)
        player2.cards = [Card(1,visible=False), Card(-1,visible=True)]
        player2.score = 99
        game.players = [player1, player2]
        game.update_scores()
        self.assertFalse(game.is_game_over())
        self.assertIsNone(game.get_game_winner())

    def test_game_over(self):
        game= Game(2)
        # Round is over and one player has more than score 100
        player1 = Player(1)
        player1.cards = [Card(0, visible=True), Card(1, visible=True)]
        player1.score = 80
        player2 = Player(2)
        player2.cards = [Card(2,visible=False), Card(-1,visible=True)]
        player2.score = 99
        game.players = [player1, player2]
        self.assertFalse(game.is_game_over())
        game.update_scores()
        self.assertEqual(81, player1.score)
        self.assertEqual(100, player2.score)
        self.assertTrue(game.is_game_over())
        winner = game.get_game_winner()
        self.assertIsInstance(winner, Player)
        self.assertEqual(1, winner.id)

    def test_update_scores_round_not_over(self):
        game= Game(2)
        player1 = Player(1)
        player1.cards = [Card(0, visible=True), Card(10, visible=False)]
        player1.score = 10
        player2 = Player(2)
        player2.cards = [Card(2,visible=False), Card(-1,visible=True)]
        player2.score = 20
        game.players = [player1, player2]
        self.assertEqual(10, player1.score)
        self.assertEqual(20, player2.score)
        game.update_scores()
        self.assertEqual(20, player1.score)
        self.assertEqual(21, player2.score)

    def test_update_scores_round_over_not_game_over(self):
        game= Game(2)
        player1 = Player(1)
        player1.cards = [Card(2, visible=True), Card(4, visible=True)]
        player1.score = 10
        player2 = Player(21)
        player2.cards = [Card(12,visible=False), Card(-2,visible=True)]
        player2.score = 20
        game.players = [player1, player2]
        self.assertEqual(10, player1.score)
        self.assertEqual(20, player2.score)
        game.update_scores()
        self.assertEqual(16, player1.score)
        self.assertEqual(30, player2.score)

    def test_update_scores_round_over_with_player_malus(self):
        game= Game(2)
        player1 = Player(1)
        player1.cards = [Card(10, visible=True), Card(10, visible=True)]
        player1.score = 10
        player2 = Player(2)
        player2.cards = [Card(12,visible=False), Card(-2,visible=True)]
        player2.score = 50
        game.players = [player1, player2]
        self.assertEqual(10, player1.score)
        self.assertEqual(50, player2.score)
        game.update_scores()
        self.assertEqual(10+2*(10+10), player1.score)
        self.assertEqual(60, player2.score)

    def test_update_scores_round_over_with_2_player_minimal(self):
        game= Game(3)
        player1 = Player(1)
        player1.cards = [Card(10, visible=True), Card(10, visible=True)]
        player1.score = 10
        player2 = Player(2)
        player2.cards = [Card(12,visible=False), Card(4,visible=True)]
        player2.score = 50
        player3 = Player(3)
        player3.cards = [Card(10,visible=False), Card(10,visible=False)]
        player3.score = 1
        game.players = [player1, player2, player3]
        self.assertEqual(10, player1.score)
        self.assertEqual(50, player2.score)
        self.assertEqual(1, player3.score)
        game.update_scores()
        self.assertEqual(10+2*(10+10), player1.score)
        self.assertEqual(66, player2.score)
        self.assertEqual(21, player3.score)

    def test_get_round_finisher(self):
        game = Game(2)
        player0 = Player(0)
        player0.cards.append(Card(10, visible=True))
        player0.cards.append(Card(2, visible=False))
        player1 = Player(1)
        player1.cards.append(Card(1, visible=True))
        player1.cards.append(Card(2, visible=True))
        player1.cards.append(Card(3, visible=True))
        player1.cards.append(Card(4, visible=True))
        game.players = [player0, player1]
        self.assertEqual(game.get_round_finisher(), player1)

    def test_get_round_finisher_none(self):
        game = Game(2)
        player0 = Player(0)
        player0.cards.append(Card(10, visible=True))
        player0.cards.append(Card(2, visible=False))
        player1 = Player(1)
        player1.cards.append(Card(1, visible=True))
        player1.cards.append(Card(2, visible=True))
        player1.cards.append(Card(3, visible=True))
        player1.cards.append(Card(4, visible=False))
        game.players = [player0, player1]
        self.assertIsNone(game.get_round_finisher())

    def test_get_round_min_scorers(self):
        game = Game(2)
        player0 = Player(0)
        player0.cards.append(Card(10, visible=True))
        player0.cards.append(Card(12, visible=False))
        player1 = Player(1)
        player1.cards.append(Card(1, visible=True))
        player1.cards.append(Card(1, visible=True))
        player1.cards.append(Card(4, visible=False))
        game.players = [player0, player1]
        self.assertListEqual(game.get_round_min_scorers(), [player1])

    def test_get_round_min_scorers_multiple(self):
        game = Game(2)
        player0 = Player(0)
        player0.cards.append(Card(2, visible=True))
        player0.cards.append(Card(2, visible=False))
        player1 = Player(1)
        player1.cards.append(Card(1, visible=True))
        player1.cards.append(Card(1, visible=True))
        player1.cards.append(Card(2, visible=False))
        game.players = [player0, player1]
        self.assertListEqual(game.get_round_min_scorers(), [player0, player1])

    def test_get_round_min_scorers_none(self):
        game = Game(2)
        game.players = []
        self.assertListEqual(game.get_round_min_scorers(), [])

    def test_get_game_winner(self):
        pass

    def test_get_min_scorer_simple(self):
        game = Game(2)
        game.players[0].score = 100
        self.assertEqual(game.get_min_scorer(game.players), game.players[1])

    def test_get_min_scorer_negative(self):
        game = Game(2)
        game.players[0].score = -2
        game.players[1].score = 2
        self.assertEqual(game.get_min_scorer(game.players).id, 0)
    
    def test_is_game_over_one_only(self):
        game = Game(2)
        game.players[0].score = 100
        self.assertTrue(game.is_game_over())

    def test_is_game_over_more(self):
        game = Game(2)
        game.players[0].score = 100
        game.players[1].score = 109
        self.assertTrue(game.is_game_over())



if __name__ == '__main__':
    unittest.main()