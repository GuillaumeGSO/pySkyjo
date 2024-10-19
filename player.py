from abc import ABC, abstractmethod
from card import Card
from typing import List, TypeVar
import random

P = TypeVar('P', bound='Player')

class Action(ABC):
    @abstractmethod
    def play(self, player: P, card: Card, rowTarget: int=0, colTarget: int=0) -> Card:
        pass

class ActionDiscardAndReturnRandom(Action):
    def play(self, player: P, card: Card, rowTarget: int=0, colTarget: int=0) -> Card: 
        print("ActionDiscardAndReturnRandom")    
        filtered_list = [card for card in player.cards if card.visible == False]
        discared_card = random.choice(filtered_list)
        player.cards.remove(discared_card)
        # swaping card
        card.row = discared_card.row
        card.column = discared_card.column
        card.visible = True
        player.cards.append(card)
        return discared_card

class ActionSwapWithTarget(Action):
    def play(self, player: P, card: Card, colTarget:int, rowTarget) -> Card: 
        print("SwapWithTarget")
        discared_card = next(card for card in player.cards if card.column==colTarget and card.row == rowTarget)
        player.cards.remove(discared_card)
        # swaping card
        card.row = discared_card.row
        card.column = discared_card.column
        card.visible = True
        player.cards.append(card)
        return discared_card
    
class ActionSwapWithHighest(Action):
    def play(self, player: P, card: Card, colTarget:int, rowTarget: int) -> Card: 
        print("ActionSwapWithHighest")
        visible_cards = [card for card in player.cards if card.visible]  
        highest_card_value = max(card.value for card in visible_cards)
        highest_card = [card for card in visible_cards if card.value == highest_card_value][0]
        player.cards.remove(highest_card)
        # swaping card
        card.row = highest_card.row
        card.column = highest_card.column
        card.visible = True
        player.cards.append(card)
        print(f"    {player.name} kept {card.value} and discared {highest_card.value} ")
        return highest_card
        




    

class Player():
    def __init__(self, id: int):
        self.id: int = id
        self.name: str = f"Player{id}"
        self.cards: List[Card] = []    # List of cards the player holds
        self.score: int = 0            # Player's score
        self.strategies = [ActionDiscardAndReturnRandom(), ActionSwapWithTarget(), ActionSwapWithHighest()]
        self.current_strategy: Action = None
    
    def __repr__(self) -> str:
        return f"Player(id='{self.id}', cards={len(self.cards)}, score={self.score})"
    
    def sum_cards_value(self):
        return sum(card.value for card in self.cards)
    
    def random_strategy(self):
        self.current_strategy = random.choice(self.strategies)
    
    def count_visible_card(self):
        return len([card for card in self.cards if card.visible==True])
    
    def get_highest_visible_card(self)-> Card:
        visible_cards = [card for card in self.cards if card.visible]  
        highest_card_value = max(card.value for card in visible_cards)
        highest_card = [card for card in visible_cards if card.value == highest_card_value][0]
        return highest_card

    
    def get_cards_in_column(self, col:int) -> List[Card]:
        return [card for card in self.cards if card.column == col]

    def find_complete_column(self):
        for i in range(4):
            cards = self.find_cards_in_column(i)
            count_visible = len([card for card in cards if card.visible==True])
            if count_visible == 3:
                return i
        return 0

    def return_two_cards(self) -> int:
        returned_cards = random.choices([card for card in self.cards if card.visible == False],k=2)
        for card in returned_cards:
            card.visible = True
        return sum(card.value for card in returned_cards)
    
    def play_turn(self, card: Card, rowTarget: int=0, colTarget:int=0) -> Card:
        
        highest_visible_card = self.get_highest_visible_card()
        if card.value < highest_visible_card.value:
            self.current_strategy = ActionSwapWithHighest()
            discard =  self.current_strategy.play(self, card, highest_visible_card.row, highest_visible_card.column)
        else:
            self.current_strategy = ActionDiscardAndReturnRandom()
            discard =  self.current_strategy.play(self, card)
    
        #check_for_columns
        return discard