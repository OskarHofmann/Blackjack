import cards
from enum import Enum, auto
from typing import Tuple, Optional
from dataclasses import dataclass
from user_interfaces import UserInterface

POINT_VALUES = {
    cards.CardValues.Ace: 11,
    cards.CardValues.Deuce: 2,
    cards.CardValues.Three: 3,
    cards.CardValues.Four: 4,
    cards.CardValues.Five: 5,
    cards.CardValues.Six: 6,
    cards.CardValues.Seven: 7,
    cards.CardValues.Eight: 8,
    cards.CardValues.Nine: 9,
    cards.CardValues.Ten: 10,
    cards.CardValues.Jack: 10,
    cards.CardValues.Queen: 10,
    cards.CardValues.King: 10
}


class UserActionsHand(Enum):
    DRAW = 1
    HOLD = 2
    SPLIT = 3


class UserActionsRoundEnd(Enum):
    CONTINUE = 1
    EXIT = 2


class Hand():
    def __init__(self) -> None:
        self.cards = []

    def __repr__(self) -> str:
        return str(self.cards)

    def __str__(self) -> str:
        cards = [str(card) for card in self.cards]
        card_str = ", ".join(cards)
        return card_str + f' ({self.get_points()})'

    def draw_card(self, shoe: cards.Deck = None) -> None:
        if shoe:
            card = shoe.draw()
        else:
            card = cards.get_random_card()
        self.cards.append(card)

    def get_points(self) -> int:
        total = 0
        n_aces = 0
        for card in self.cards:
            total += POINT_VALUES[card.value]
            # count aces as each ace can be counted as 1 if total is above 21
            if card.value == cards.CardValues.Ace:
                n_aces += 1

        if total > 21:
            # count ace(s) as 1 instead of 11 (-10) until total <= 21 or no aces left
            while n_aces > 0 and total > 21:
                total -= 10
                n_aces -= 1              

        return total
    
    def is_splittable(self) -> bool: 
        # hand is splittable if and only if it contains two cards with the same value
        if len(self.cards) != 2:
            return False
        return (POINT_VALUES[self.cards[0].value] == POINT_VALUES[self.cards[1].value])
    

    def is_bust(self) -> bool:
        return (self.get_points > 21)
    
    
    def is_blackjack(self) -> bool:
        return ((len(self.cards) == 2) and (self.get_points == 21))


@dataclass
class GameState():
    money: int = 0
    player_hands: Optional[list[Hand]] = None
    dealer_hand: Optional[Hand] = None
    current_hand: int = -1

    def reset_hands(self) -> None:
        self.player_hands = None
        self.dealer_hand = None
        self.current_hand = -1

    def update_hands(self, player_hands: list[Hand], dealer_hand: Hand) -> None:
        self.player_hands = player_hands
        self.dealer_hand = dealer_hand



class Game():   
    
    # n_decks = 0 (default) draws each card completely randomly and independently
    def __init__(self, user_interface: UserInterface, n_decks: int = 0) -> None:       

        if not isinstance(n_decks, int) or n_decks < 0:
            raise ValueError('n_decks must be an integer >= 0')
        elif n_decks == 0:
            self.shoe = None
        else:
            self.shoe = cards.Shoe(n_decks)
        
        self.user_interface = user_interface
        self._running = True
        self.game_state = GameState()
        
        while(self._running):
            round = self.Round(self.game_state, self.user_interface, self.shoe)
            self._running, money_won = round.play()
            self.game_state.money += money_won
            self.game_state.reset_hands()
            # self.UI.money = self.money    

        
    class Round():        

        def __init__(self, game_state: GameState, user_interface: UserInterface, shoe: cards.Deck = None) -> None:
            # a player can have several hands when he splits, the dealer always has 1 hand
            player_hands = [Hand()]
            dealer_hand = Hand()
            self.shoe = shoe
            self.game_state = game_state
            self.ui = user_interface
            
            player_hands[0].draw_card(self.shoe)
            dealer_hand.draw_card(self.shoe)
            player_hands[0].draw_card(self.shoe)
          
            # The dealer would get his 2nd card upside down at this point, but it does not matter if
            # he draws it now or later (during play()).
            # Drawing it later also allows to use standard __str__ method the dealer's hand 
            # self.dealer_hand.draw_card(self.shoe)

            self.game_state.update_hands(self.player_hands, self.dealer_hand)


        def play(self) -> Tuple[bool, int]:                   
            self.game_state.current_hand = 0
                    
            # iterate over each hand (list of hands can grow when splitting)
            while self.game_state.current_hand < len(self.game_state.player_hands):
                hand_over = False
                player_hand = self.game_state.player_hands[self.game_state.current_hand]

                while not hand_over:
                    self.ui.show_hand(self.game_state)
                    user_input = self.ui.get_user_input_hand(self.game_state)

                    if user_input == UserActionsHand.DRAW:
                        player_hand.draw_card(self.shoe)
                        hand_over = player_hand.is_bust()
                    elif user_input == UserActionsHand.HOLD:
                        hand_over = True
                    elif user_input == UserActionsHand.SPLIT:
                        self.split_hand()
                    else:
                        raise RuntimeError('Unexpected user action')
                    
                    self.update_game_state()
                
                self.ui.hand_summary()
                    
            self.draw_dealer()
            money_won = sum(self.evaluate_hands())
            self.ui.round_summary()

            user_input = self.ui.get_user_input_round_end()
            continue_game = (user_input == UserActionsRoundEnd.CONTINUE)

            return continue_game, money_won
        

        def split_hand(self):
            pass

        def evaluate_hands(self) -> list[int]:
            pass

        def update_game_state(self):
            # call game_state.update_hands
            pass

        def draw_dealer(self):
            pass







    
    



