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

    draw: draw a card from the current deck
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

##### Class Deck
class Shoe:
    """
    Represents the shoe, which is a gaming device, mainly used
    in casinos, to hold multiple decks of playing cards.

    ----
    attributes:
    num_deck: the number of decks of playing cards, default with 6,
    recommend values: {2, 4, 6, 8}

    shoe_list: list of Card objects

    ----
    methods:
    shuffle: shuffle the current shoe

    draw: draw a card from the current shoe
    """
    def __init__(self, num_decks:int=6):
        """
        ----
        parameters:
        num_decks: the number of decks of playing cards, default with 6,
        recommend values: {2, 4, 6, 8}

        """
        self.num_decks = num_decks
        self.__shuffle_point = None  # index of shoe list
        self.shoe_list = self.__build()
        self.shuffle()  # shuffle the initial shoe and set penetration

    def __build(self) -> list:
        """
        Generate a shoe of playing Card objects

        ----
        return:
        shoe_list: list of Card objects
        """
        shoe_list = []
        for i in range(self.num_decks):
            shoe_list += Deck().deck_list
        return shoe_list

    def shuffle(self):
        """
        Shuffle the deck, using random.shuffle() method
        """
        random.shuffle(self.shoe_list)
        self.__set_penetration()

    def draw(self):
        """
        Draw a card from the current shoe, i.e. the last element
        in the shoe_list

        ----
        return the last element in shoe_list, a Card object
        """
        return self.shoe_list.pop()

    def __set_penetration(self):
        """
        Set penetration every time the shoe is shuffled. This private
        method is only used in self.shuffle()
        """
        shuffle_point_pct = random.uniform(0.25, 0.5)  # TODO
        self.__shuffle_point = round(shuffle_point_pct * 52 * self.num_decks)

    def __check_penetration(self):
        """
        Check if the shoe reaches the shuffle point. Check every time a
        card is drawn
        """
        if len(self.shoe_list) <= self.__shuffle_point:
            self.shuffle()
