import cards
from typing import Tuple, Optional
from dataclasses import dataclass
from user_interfaces import UserInterface
from user_actions import UserActionsHand, UserActionsRoundEnd
import numpy as np

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
        return (self.get_points() > 21)
    
    
    def is_blackjack(self) -> bool:
        return ((len(self.cards) == 2) and (self.get_points() == 21))
    
    # "Double down on any two"
    def can_be_doubled(self) -> bool:
        return len(self.cards) == 2


@dataclass
class GameState():
    money: float = 0
    player_hands: Optional[list[Hand]] = None
    dealer_hand: Optional[Hand] = None
    current_hand: int = -1
    bets: Optional[list[int]] = None


    def reset_hands(self) -> None:
        self.player_hands = None
        self.dealer_hand = None
        self.current_hand = -1
        self.bets = None

    # def update_hands(self, player_hands: list[Hand], dealer_hand: Hand) -> None:
    #     self.player_hands = player_hands
    #     self.dealer_hand = dealer_hand

    def get_current_hand(self) -> Hand:
        return self.player_hands[self.current_hand]



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
        
        self.user_interface.game_summary(self.game_state)

        
    class Round():        

        def __init__(self, game_state: GameState, user_interface: UserInterface, shoe: cards.Deck = None) -> None:
            # a player can have several hands when he splits, the dealer always has 1 hand
            player_hands = [Hand()]
            dealer_hand = Hand()
            self.shoe = shoe
            self.game_state = game_state
            self.ui = user_interface

            self.bet = 1 # could be a variable input in the future
            self.game_state.bets = [self.bet]
            
            player_hands[0].draw_card(self.shoe)
            dealer_hand.draw_card(self.shoe)
            player_hands[0].draw_card(self.shoe)
          
            # The dealer would get his 2nd card upside down at this point, but it does not matter if
            # he draws it now or later (during play()).
            # Drawing it later also allows to use standard __str__ method the dealer's hand 
            # self.dealer_hand.draw_card(self.shoe)

            self.game_state.player_hands = player_hands
            self.game_state.dealer_hand = dealer_hand


        def play(self) -> Tuple[bool, int]:                   
            self.game_state.current_hand = 0
                    
            # iterate over each hand (list of hands can grow when splitting)
            while self.game_state.current_hand < len(self.game_state.player_hands):
                hand_over = False
                player_hand = self.game_state.get_current_hand()

                if player_hand.is_blackjack():
                    hand_over = True

                while not hand_over:
                    self.ui.show_hand(self.game_state)
                    user_input = self.ui.get_user_input_hand(self.game_state)

                    if user_input == UserActionsHand.DRAW:
                        player_hand.draw_card(self.shoe)
                        hand_over = (player_hand.is_bust() or player_hand.is_blackjack())
                    elif user_input == UserActionsHand.STAND:
                        hand_over = True
                    elif user_input == UserActionsHand.DOUBLE_DOWN:
                        player_hand.draw_card(self.shoe)
                        self.game_state.bets[self.game_state.current_hand] *= 2
                        hand_over = True
                    elif user_input == UserActionsHand.SPLIT:
                        self.split_hand()
                    else:
                        raise RuntimeError('Unexpected user action')
                    
                self.ui.hand_summary(self.game_state)
                self.game_state.current_hand += 1
                    
            self.draw_dealer()
            hand_results = self.evaluate_hands()
            self.ui.round_summary(self.game_state, hand_results)

            user_input = self.ui.get_user_input_round_end()
            continue_game = (user_input == UserActionsRoundEnd.CONTINUE)

            return continue_game, sum(hand_results)
        

        def split_hand(self):
            hand = self.game_state.get_current_hand()
            if not hand.is_splittable():
                raise RuntimeError(f'Trying to split unsplittable hand: {hand}')
            
            # remove card from first hand and create new hand with that card
            card_to_split = hand.cards.pop()
            new_hand = Hand()
            new_hand.cards.append(card_to_split)

            # draw one new card for each of the hands
            hand.draw_card(self.shoe)
            new_hand.draw_card(self.shoe)

            # add new hand to list of player hands
            self.game_state.player_hands.append(new_hand)
            # use bet of current hand as bet for new hand
            self.game_state.bets.append(self.game_state.bets[self.game_state.current_hand])


        def evaluate_hands(self) -> list[float]:
            results = []
            dealer_hand = self.game_state.dealer_hand
            bets = self.game_state.bets
            
            # go through all rules for BlackJack regarding winning/loosing
            for hand, bet in zip(self.game_state.player_hands, bets):
                # bust hand always looses player bet
                if hand.is_bust():
                    winnings = -1
                # Blackjack without dealer Blackjack wins 3:2
                elif hand.is_blackjack() and not dealer_hand.is_blackjack():
                    winnings = 1.5
                # player wins when dealer is bust (if player is also bust, player looses, but already covered in previous if statement)
                elif dealer_hand.is_bust():
                    winnings = 1
                # dealer Blackjack wins if player does not have his own blackjack
                elif  dealer_hand.is_blackjack() and not hand.is_blackjack():
                    winnings = -1
                # otherwise compare point values (both player and dealer having a Blackjack is the same as both just having 21)
                else:
                    winnings = 1 * np.sign(hand.get_points() - dealer_hand.get_points()) # +1 if player > dealer, -1 if player < dealer, 0 otherwise
            
                results.append(winnings*bet)
            
            return results
        

        def draw_dealer(self) -> None:
            # check if dealer even has to draw (any hand that is not bust)
            dealer_draws = False
            for hand in self.game_state.player_hands:
                if not hand.is_bust():
                    dealer_draws = True
                    break
            # end function if hand outcome does not depend on dealer draw
            if not dealer_draws:
                return
            
            dealer_hand = self.game_state.dealer_hand
            while not (dealer_hand.is_bust() or dealer_hand.get_points() >= 17):
                dealer_hand.draw_card()










    
    



