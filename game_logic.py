import cards
from enum import Enum, auto
from typing import Tuple

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

class UserActions(Enum):
    DRAW = 1
    HOLD = 2
    SPLIT = 3

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

    


class Game():   
    
    # n_decks = 0 (default) draws each card completely randomly and independently
    def __init__(self, n_decks: int = 0) -> None:       

        if not isinstance(n_decks, int) or n_decks < 0:
            raise ValueError('n_decks must be an integer >= 0')
        elif n_decks == 0:
            self.shoe = None
        else:
            self.shoe = cards.Shoe(n_decks)
        
        self._running = True
        self.money = 0

        while(self._running):
            round = self.Round()
            self._running, money_won = round.play()
            self.money += money_won
            # self.UI.money = self.money    

        
    class Round():

        # TODO: Move to UI and define game_Logic constants as return values
        PLAYER_CHOICES_WITHOUT_SPLIT = ['1: Draw', '2: Hold']
        PLAYER_CHOICES_WITH_SPLIT = ['1: Draw', '2: Hold', '3: Split']

        def __init__(self, shoe: cards.Deck = None) -> None:
            # a player can have several hands when he splits, the dealer always has 1 hand
            self.player_hands = [Hand()]
            self.dealer_hand = Hand()
            self.shoe = shoe
            
            self.player_hands[0].draw_card(self.shoe)
            self.dealer_hand.draw_card(self.shoe)
            self.player_hands[0].draw_card(self.shoe)
            
            # The dealer would get his 2nd card upside down at this point, but it does not matter if
            # he draws it now or later (during play()).
            # Drawing it later also allows to use standard __str__ method the dealer's hand 
            # self.dealer_hand.draw_card(self.shoe)

        def play(self) -> Tuple[bool, int]:                   
            # self.UI.update()
            print("Player: ", self.player_hands[0])
            print("Dealer: ", self.dealer_hand)

            for player_hand in self.player_hands:
                # self.UI.user_input()
                hand_over = False

                while not hand_over:

                    if player_hand.is_splittable():
                        choices = self.PLAYER_CHOICES_WITH_SPLIT
                    else:
                        choices = self.PLAYER_CHOICES_WITHOUT_SPLIT
                        
                    print(*choices, sep = '\n')
                    while True:
                        choice = int(input())

                pass    

            return False, 0
        

        def split_hand(self):
            pass

        def evaluate_hands(self):
            pass






    
    



