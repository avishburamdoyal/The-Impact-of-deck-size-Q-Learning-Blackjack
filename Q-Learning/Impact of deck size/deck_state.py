#Required packages
import pandas as pd
import numpy as np

#Defining class deck
class Deck:

    #Drawing new deck 
    def __init__(self):
        deck_list = []
        for i in range(2, 10):
            deck_list  += [str(i)] * 4 * 21  # 6-deck Blackjack game
        deck_list  += ['10'] * 16 * 21 + ['A'] * 4 * 21
        self.deck = deck_list 

    #Shuffle deck
    def shuffle(self):
        shuffle_factor = np.random.randint(15, 20)
        for _ in range(shuffle_factor):
            np.random.shuffle(self.deck)

    #Drawing new card 
    def draw(self):
        return self.deck.pop(0)

    #Number of remaining cards in deck 
    def size(self):
        return len(self.deck)
