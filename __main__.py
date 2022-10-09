import cards

if __name__ == '__main__':
    deck = cards.Shoe()
    for _ in range(10):
        print(deck.draw())
    print(len(deck.cards))