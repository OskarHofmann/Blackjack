from abc import ABC, abstractmethod
import os
from game_logic import UserActionsHand, UserActionsRoundEnd, GameState

class UserInterface(ABC):    

    @abstractmethod
    def show_hand(self, game_state: GameState) -> None:
        ...

    @abstractmethod
    def game_summary(self, game_state: GameState) -> None:
        ...

    @abstractmethod
    def round_summary(self, game_state: GameState) -> None:
        ... 

    @abstractmethod
    def hand_summary(self, game_state: GameState) -> None:
        ... 

    @abstractmethod
    def show_player_options_hand(self, game_state: GameState) -> None:
        ...

    @abstractmethod
    def get_user_input_hand(self, game_state: GameState) -> UserActionsHand:
        ...

    @abstractmethod
    def get_user_input_round_end(self, game_state: GameState) -> UserActionsRoundEnd:
        ...

    

class ConsoleOutput(UserInterface):

    # order is fixed as of Python 3.7+
    PLAYER_CHOICES_WITHOUT_SPLIT = {UserActionsHand.DRAW: 'Draw', UserActionsHand.HOLD: 'Hold'}
    PLAYER_CHOICES_WITH_SPLIT = {UserActionsHand.DRAW: 'Draw', UserActionsHand.HOLD: 'Hold', UserActionsHand.SPLIT: 'Split'}

    def update(self):
        os.system('cls')
        print("Player Hand:", self.game_stats["player hands"][-1])
        print("Dealer Hand:", self.game_stats["dealer hand"])

    def show_hand(self, game_state: GameState) -> None:
        print("Player: ", game_state.player_hands[game_state.current_hand])
        print("Dealer: ", game_state.dealer_hand)

    def get_user_input_hand(self, game_state: GameState) -> UserActionsHand:
        self.show_player_options_hand(game_state)
        while True:
            choice = int(input())

    def show_player_options_hand(self, game_state: GameState) -> None:
        # determine if hand is splittable and determine if the option to split should be shown
        if game_state.player_hands[game_state.current_hand].is_splittable():
            choices = self.PLAYER_CHOICES_WITH_SPLIT
        else:
            choices = self.PLAYER_CHOICES_WITHOUT_SPLIT        
        print(*choices, sep = '\n')

    def print_choices(hand_is_splittable: bool) -> None:
        pass
        