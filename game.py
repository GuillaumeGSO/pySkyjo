from typing import List, Optional
import random
from player import Player
from card import Card




class Game:
    def __init__(self, number_players: int):
        self.number_players: int = number_players  # Number of players in the game
        self.players: List[Player] = []
        self.deck: List[Card] = []
        self.currentPlayer: Player = None
        self.next_card: Card = None
        self.playable_card: Card = None
        self.init_game()

    def generate_players(self) -> List[Player]:
        return [Player("Player" + str(p)) for p in range(self.number_players)]

    def reorder_players(self, start_player: Player) -> List[Player]:
        if start_player not in self.players:
            return self.players  # Return original list if start_player is not in the list
        start_index = self.players.index(start_player)
        self.players =  self.players[start_index:] + self.players[:start_index]
        return self.players

    def generate_deck(self) -> List[Card]:
        listOfCards = [x for x in range(-2, 13)]
        deck = listOfCards * 10  # Create the deck
        random.shuffle(deck)  # Shuffle the deck
        return [Card(value) for value in deck]

    def init_game(self):
        self.players = self.generate_players()

    def init_round(self):
        self.deck = self.generate_deck()
        start_player = None
        max_score = -999
        for player in self.players:
            player.cards.clear()
            for i in range(12):
                card = self.deck.pop(0)
                card.column = i % 4
                card.row = i % 3
                player.cards.append(card)
            returned_card_value = player.return_two_cards()
            if returned_card_value > max_score:
                max_score = returned_card_value
                start_player = player
        
        self.reorder_players(start_player)
        self.playable_card = self.deck.pop(0)        

    def update_scores(self):
        round_finisher = self.get_round_finisher()
        minimal_scorers = self.get_round_min_scorer()
        for player in self.players:
            player.score += player.sum_cards_value()
            if player == round_finisher and not (player in minimal_scorers):
                player.score += player.sum_cards_value()
    
    def give_one_card_from_deck(self) -> Card:
        return self.deck.pop(0)

    def get_round_finisher(self) -> Optional[Player]:
        for player in self.players:
            if all(card.visible for card in player.cards):
                return player
        return None
    
    def get_round_min_scorer(self) -> List[Player]:
        min_score = float('inf')
        min_scorers = []
        #Search minimal score
        for player in self.players:
            player_cards_value = player.sum_cards_value()
            if player_cards_value < min_score:
                min_score = player_cards_value
        
        #Fetch all players with minimal score
        for player in self.players:
            player_cards_value = player.sum_cards_value()
            if (player_cards_value == min_score):
                min_scorers.append(player)
    
        return min_scorers

    def get_game_winner(self) -> Optional[Player]:
        if self.is_game_over():
            return self.get_min_score(self.players)
        return None
    
    def get_min_score(self,players: List[Player]) -> Player:
        return min(players, key=lambda player: player.score)
    
    def is_game_over(self) -> bool:
        return any(player.score >= 1000 for player in self.players)


               




