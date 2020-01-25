##### Configuration
import numpy as np
import random


##### Class Card
class Card:
    """
    Generate a card based on suit and value

    ----
    method:
    show: show the card
    """

    def __init__(self, suit:str, val:int):
        """
        ----
        parameters:
        suit: suit of the card
        val: value of the card
        """
        self.suit = suit
        self.value = val

    def show(self):
        """
        Show the suit and value of the card
        """
        print(f'{self.value} of {self.suit}')

##### Class Deck
class Deck:
    """
    Generate one deck of cards

    ----
    attributes:
    deck_list: list of Card object

    ----
    methods:
    __build: generate one deck of cards, return as list

    shuffle: shuffle the current deck

    show: show the current deck

    """
    def __init__(self, shuffle:bool=True):
        """
        ----
        paramters:
        shuffle: shuffle the initial deck or not
        """
        self.deck_list = self.__build()
        if shuffle:
            self.shuffle()

    def __build(self) -> list:
        """
        Generate one deck of cards

        ----
        return:
        deck_list: list of 52 Card objects
        """
        suit_list = ['Spades', 'Clubs', 'Diamonds', 'Hearts']
        return [Card(s, v) for s in suit_list for v in range(1, 14)]

    def shuffle(self):
        """
        Shuffle the deck, using random.shuffle() method
        """
        random.shuffle(self.deck_list)

    def show(self, num_cards:int=13):
        """
        Show the first {num_cards} cards in the deck

        ----
        parameter:
        num_cards: the number of cards to show, default 10
        if num_cards <= 0, show all the cards

        """
        if num_cards <= 0 or num_cards > len(self.deck_list):
            num_cards = len(self.deck_list)
        for i in range(num_cards):
            self.deck_list[i].show()  # Call the show() method of Card object

    def draw(self):
        """
        Draw a card from the current deck

        ----
        return the last element in deck_list, a Card object
        """
        return self.deck_list.pop()
