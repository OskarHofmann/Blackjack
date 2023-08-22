from __future__ import annotations
from abc import ABC, abstractmethod
import os
from user_actions import UserActionsHand, UserActionsRoundEnd

# avoid circular import, GameState is only used as an annotation
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_logic import GameState


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
        hand_is_splittable = game_state.player_hands[game_state.current_hand].is_splittable()
        self.show_player_options_hand(hand_is_splittable)

        while True:
            choice = int(input())
        #TODO: Handle non int inputs and check for valid input

    #TODO: use boolean is_splittable as input only
    def show_player_options_hand(self, hand_is_splittable: bool) -> None:
        # determine if hand is splittable and determine if the option to split should be shown
        if hand_is_splittable:
            choices = self.PLAYER_CHOICES_WITH_SPLIT
        else:
            choices = self.PLAYER_CHOICES_WITHOUT_SPLIT        
        for choice, text in choices.items():
            print(f'{choice.value}: {text}')

    def game_summary(self, game_state: GameState) -> None:
        pass

    def get_user_input_round_end(self, game_state: GameState) -> UserActionsRoundEnd:
        pass

    def hand_summary(self, game_state: GameState) -> None:
        pass

    def round_summary(self, game_state: GameState) -> None:
        pass
    


