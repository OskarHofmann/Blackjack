import cards

POINT_VALUES = {
    "Ace": 11,
    "Deuce": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
    "Six": 6,
    "Seven": 7,
    "Eight": 8,
    "Nine": 9,
    "Ten": 10,
    "Jack": 10,
    "Queen": 10,
    "King": 10
}

class Hand():
    def __init__(self):
        self.cards = []

    def __repr__(self):
        return str(self.cards)

    def __str__(self):
        cards = [str(card) for card in self.cards]
        card_str = ", ".join(cards)
        return card_str + f' ({self.get_points()})'

    def draw_card(self, shoe: cards.Deck = None):
        if shoe:
            card = shoe.draw()
        else:
            card = cards.get_random_card()
        self.cards.append(card)

    def get_points(self):
        total = 0
        n_aces = 0
        for card in self.cards:
            total += POINT_VALUES[card.value.name]
            # count aces as each ace can be counted as 1 if total is above 21
            if card.value == cards.CardValues.Ace:
                n_aces += 1

        if total > 21:
            # count ace(s) as 1 instead of 11 (-10) until total <= 21 or no aces left
            while n_aces > 0 and total > 21:
                total -= 10
                n_aces -= 1              

        return total
    
    def is_splittable(self): 
        # hand is splittable if and only if it contains two cards with the same value
        if len(self.cards) != 2:
            return False
        return (POINT_VALUES[self.cards[0].value] == POINT_VALUES[self.cards[1].value])

    


class Game():   
    
    # n_decks = 0 (default) draws each card completely randomly and independently
    def __init__(self, n_decks: int = 0):       

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

        def __init__(self, shoe: cards.Deck = None):
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

        def play(self):                   
            # self.UI.update()
            print("Player: ", self.player_hands[0])
            print("Dealer: ", self.dealer_hand)

            for player_hand in self.player_hands:
                # self.UI.user_input()
                choice_str = '1: Draw \n2:Hold'
                if player_hand.is_splittable():
                    choice_str += '\n'
                while True:

                    choice = int(input()

                pass    

            return False, 0



    
    



