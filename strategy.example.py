from abc import ABC, abstractmethod
import random

# Strategy interface
class ActionStrategy(ABC):
    @abstractmethod
    def execute(self, player_name):
        pass

# Concrete strategies
class Action1Strategy(ActionStrategy):
    def execute(self, player_name):
        return f"{player_name} performs action 1"

class Action2Strategy(ActionStrategy):
    def execute(self, player_name):
        return f"{player_name} performs action 2"

class Action3Strategy(ActionStrategy):
    def execute(self, player_name):
        return f"{player_name} performs action 3"

# Context
class Player:
    def __init__(self, name):
        self.name = name
        self.strategies = [Action1Strategy(), Action2Strategy(), Action3Strategy()]
        self.current_strategy = None

    def set_strategy(self, strategy):
        self.current_strategy = strategy

    def random_strategy(self):
        self.current_strategy = random.choice(self.strategies)

    def perform_action(self):
        if self.current_strategy:
            return self.current_strategy.execute(self.name)
        else:
            return f"{self.name} has no action strategy set"

# Example usage
player = Player("Alice")

print("Using specific strategies:")
player.set_strategy(Action1Strategy())
print(player.perform_action())
player.set_strategy(Action2Strategy())
print(player.perform_action())

print("\nUsing random strategies:")
for _ in range(3):
    player.random_strategy()
    print(player.perform_action())