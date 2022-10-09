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

    def draw_card(self, shoe: cards.Deck = None):
        if shoe:
            card = shoe.draw()
        else:
            card = cards.get_random_card()
        self.cards.append(card)
    


class Game():
    # n_decks = 0 (default) draws each card completely randomly and independently
    def __init__(self, n_decks: int = 0):       

        if not isinstance(n_decks, int) or n_decks < 0:
            raise ValueError('n_decks must be an integer >= 0')
        elif n_decks == 0:
            self.shoe = None
        else:
            self.shoe = cards.Shoe(n_decks)
        
        #TODO: make this part of a round, not the game
        
        # a player can have several hands when he splits, the dealer always has 1 hand
        self.player_hands = [Hand()]
        self.dealer_hand = Hand()
        
        self.player_hands[0].draw_card(self.shoe)
        self.dealer_hand.draw_card(self.shoe)
        self.player_hands[0].draw_card(self.shoe)
        self.dealer_hand.draw_card(self.shoe)
        
        #self.UI.update()

    
    



