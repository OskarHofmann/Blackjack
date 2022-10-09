from enum import Enum, auto
import random

class CardSuits(Enum):
    Clubs = auto() # 1
    Spades = auto() # 2
    Hearts = auto() # 3
    Diamonds = auto() # 4

class CardValues(Enum):
    Ace = auto() # 1
    Deuce = auto() # 2
    Three = auto() # 3
    Four = auto() # 4
    Five = auto() # 5
    Six = auto() # 6
    Seven = auto() # 7
    Eight = auto() # 8
    Nine = auto() # 9
    Ten = auto() # 10
    Jack = auto() # 11
    Queen = auto() # 12
    King = auto() # 13

class Card:
    def __init__(self, suit: CardSuits, value: CardValues):
        self.suit = suit
        self.value = value

    def __str__(self):
        return f"{self.value.name} of {self.suit.name}"

class Deck:
    def __init__(self, shuffle: bool = True):
        self.cards = [Card(suit, value) for suit in CardSuits for value in CardValues]
        if shuffle:
            random.shuffle(self.cards)

# several decks shuffled together
class Shoe:
    def __init__(self, number_of_decks: int = 8):
        self.cards = []
        for _ in range(number_of_decks):
            # create unshuffled deck as the whole shoe is shuffled later
            deck = Deck(shuffle = False) 
            self.cards.append(deck)
        random.shuffle(self.cards)
    
