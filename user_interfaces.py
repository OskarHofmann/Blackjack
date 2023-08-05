from abc import ABC, abstractmethod
import os
from game_logic import UserActions, GameState

class UserInterface(ABC):    

    @abstractmethod
    def update_hand(self, game_state: GameState):
        ...

    @abstractmethod
    def game_summary(self, game_state: GameState):
        ...

    @abstractmethod
    def show_player_options_hand(self, game_state: GameState):
        ...

    @abstractmethod
    def get_user_input_hand(self, game_state: GameState):
        ...

    @abstractmethod
    def get_user_input_round_end(self, game_state: GameState):
        ...

    

class ConsoleOutput(UserInterface):

    def update(self):
        os.system('cls')
        print("Player Hand:", self.game_stats["player hands"][-1])
        print("Dealer Hand:", self.game_stats["dealer hand"])