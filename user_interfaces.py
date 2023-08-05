from abc import ABC, abstractmethod
import os

class UserInterface(ABC):

    def __init__(self):
        self.game_stats = {
            "player hands": None,
            "dealer hand": None,
            "money": 0
        }

    @abstractmethod
    def update_hand(self):
        ...

    @abstractmethod
    def game_summary(self):
        ...

    @abstractmethod
    def show_player_options_hand(self):
        ...

    @abstractmethod
    def get_user_input_hand(self):
        ...

    @abstractmethod
    def get_user_input_round_end(self):
        ...

    

class ConsoleOutput(UserInterface):

    def update(self):
        os.system('cls')
        print("Player Hand:", self.game_stats["player hands"][-1])
        print("Dealer Hand:", self.game_stats["dealer hand"])