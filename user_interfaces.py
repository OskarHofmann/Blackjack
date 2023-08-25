from __future__ import annotations
from abc import ABC, abstractmethod
import os
from user_actions import UserActionsHand, UserActionsRoundEnd
from time import sleep

# avoid circular import, GameState is only used as an annotation
from typing import TYPE_CHECKING, Dict, List
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
    def round_summary(self, game_state: GameState, money_won: List[int]) -> None:
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
    def get_user_input_round_end(self) -> UserActionsRoundEnd:
        ...

    

class ConsoleOutput(UserInterface):

    # order is fixed as of Python 3.7+
    PLAYER_CHOICES_WITHOUT_SPLIT = {UserActionsHand.DRAW: 'Draw', UserActionsHand.STAND: 'Stand'}
    PLAYER_CHOICES_WITH_SPLIT = {UserActionsHand.DRAW: 'Draw', UserActionsHand.STAND: 'Stand', UserActionsHand.SPLIT: 'Split'}

    PLAYER_CHOICES_ROUND_END ={UserActionsRoundEnd.CONTINUE: 'Continue', UserActionsRoundEnd.EXIT: 'Exit'}
    
    WRONG_INPUT_TEXT = "Please input a number based on the option above."

    HAND_IS_BUST_TEXT = "Over 21! Hand is bust. All bets are lost."
    HAND_IS_BLACKJACK_TEXT = "Blackjack! Player wins 3:2."

    END_OF_ROUND_TEXT = "End of round!"
    PLAYER_WINS_TEXT = "Player wins. Money won: "
    PLAYER_LOOSES_TEXT = "Player looses. Money lost: "
    TIE_TEXT = "Tie! No money won or lost."
    

    # def update(self):
    #     os.system('cls')
    #     print("Player Hand:", self.game_stats["player hands"][-1])
    #     print("Dealer Hand:", self.game_stats["dealer hand"])

    def show_hand(self, game_state: GameState) -> None:
        os.system('cls')
        print("Player: ", game_state.player_hands[game_state.current_hand])
        print("Dealer: ", game_state.dealer_hand)


    def get_user_input_hand(self, game_state: GameState) -> UserActionsHand:
        if game_state.player_hands[game_state.current_hand].is_splittable():
            valid_choices = self.PLAYER_CHOICES_WITH_SPLIT
        else:
            valid_choices = self.PLAYER_CHOICES_WITHOUT_SPLIT

        self.show_player_options_hand(valid_choices)

        while True:
            try:
                choice = int(input())
            except ValueError:
                print(self.WRONG_INPUT_TEXT)
                continue
            
            if choice in valid_choices.keys():
                return UserActionsHand(choice)
            else:
                print(self.WRONG_INPUT_TEXT)
                continue # just for clarity, could be left out


    def show_player_options_hand(self, choices: Dict[UserActionsHand, str]) -> None:           
        for choice, text in choices.items():
            print(f'{choice.value}: {text}')


    def game_summary(self, game_state: GameState) -> None:
        os.system('cls')
        print("Game over!")
        print(f"Total money won/lost: {game_state.money}")


    def get_user_input_round_end(self) -> UserActionsRoundEnd:
        self.show_player_options_round_end()

        while True:
            try:
                choice = int(input())
            except ValueError:
                print(self.WRONG_INPUT_TEXT)
                continue
            
            if choice in self.PLAYER_CHOICES_ROUND_END.keys():
                return UserActionsRoundEnd(choice)
            else:
                print(self.WRONG_INPUT_TEXT)
                continue # just for clarity, could be left out


    def show_player_options_round_end(self) -> None:
        for choice, text in self.PLAYER_CHOICES_ROUND_END.items():
            print(f'{choice.value}: {text}')
        

    def hand_summary(self, game_state: GameState) -> None:
        # if only one hand was played (no split hand), there is no need to specify the number of the hand
        if len(game_state.player_hands) > 1:
            print(f'End of hand {game_state.current_hand + 1} :')
        self.show_hand(game_state)

        # End of hand text for hands that are bust or blackjack
        player_hand = game_state.player_hands[game_state.current_hand]
        if player_hand.is_bust():
            print(self.HAND_IS_BUST_TEXT)
        elif player_hand.is_blackjack():
            print(self.HAND_IS_BLACKJACK_TEXT)
        
        sleep(2)
        

    def round_summary(self, game_state: GameState, money_won: List[int]) -> None:
        os.system('cls')
        print(self.END_OF_ROUND_TEXT)
        print("")
        print("Dealer: ", game_state.dealer_hand, "\n")
        for index, hand in enumerate(game_state.player_hands):
            print(f"Player hand #{index + 1}: ", hand)
            earnings = money_won[index]
            if earnings > 0:
                print(self.PLAYER_WINS_TEXT, earnings)
            elif earnings < 0:
                print(self.PLAYER_LOOSES_TEXT, earnings*-1)
            else:
                print(self.TIE_TEXT)
            print("")
            sleep(1)




    


