from __future__ import annotations
from abc import ABC, abstractmethod
import os
from user_actions import UserActionsHand, UserActionsRoundEnd

# avoid circular import, GameState is only used as an annotation
from typing import TYPE_CHECKING, Dict
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
    
    wrong_input_text = "Please input a number based on the option above."

    def update(self):
        os.system('cls')
        print("Player Hand:", self.game_stats["player hands"][-1])
        print("Dealer Hand:", self.game_stats["dealer hand"])

    def show_hand(self, game_state: GameState) -> None:
        print("Player: ", game_state.player_hands[game_state.current_hand])
        print("Dealer: ", game_state.dealer_hand)


    def get_user_input_hand(self, game_state: GameState) -> UserActionsHand:
        if game_state.player_hands[game_state.current_hand].is_splittable():
            valid_choices = self.PLAYER_CHOICES_WITH_SPLIT
        else:
            valid_choices = self.PLAYER_CHOICES_WITHOUT_SPLIT

        self.show_player_options_hand(valid_choices)
        print(valid_choices.keys())

        while True:
            try:
                choice = int(input())
            except ValueError:
                print(self.wrong_input_text)
                continue
            
            if choice in valid_choices.keys():
                return UserActionsHand(choice)
            else:
                print(self.wrong_input_text)
                continue # just for clarity, could be left out


    def show_player_options_hand(self, choices: Dict[UserActionsHand, str]) -> None:           
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
    


