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
        return ", ".join(cards)

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
            if card.value.name == "Ace":
                n_aces += 1

        if total > 21:
            # count ace(s) as 1 instead of 11 (-10) until total <= 21 or no aces left
            while n_aces > 0 and total > 21:
                total -= 10
                n_aces -= 1              

        return total
    


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
        def __init__(self, shoe: cards.Deck = None):
            # a player can have several hands when he splits, the dealer always has 1 hand
            self.player_hands = [Hand()]
            self.dealer_hand = Hand()
            self.shoe = shoe
            
            self.player_hands[0].draw_card(self.shoe)
            self.dealer_hand.draw_card(self.shoe)
            self.player_hands[0].draw_card(self.shoe)
            self.dealer_hand.draw_card(self.shoe)

        def play(self):                   
            #self.UI.update()
            print(self.player_hands[0])
            print(self.dealer_hand.cards[0])

            for player_hand in self.player_hands:
                pass    

            return False, 0



    
    



