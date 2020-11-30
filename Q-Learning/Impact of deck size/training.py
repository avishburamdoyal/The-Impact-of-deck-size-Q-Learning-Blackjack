#Importing classes
from deck_state import Deck
from env_state import handState
import pandas as pd
import numpy as np

#Training RL agent 
class Train_agent:
    
    def __init__(self, alpha, gamma):
        self.alpha = alpha # learning rate
        self.gamma = gamma
        self.state = handState()
        self.deck = Deck()
        self.deck.shuffle()
        self.Q = np.matrix(np.zeros([len(self.state.current_states)*1801, 4]))

    #Function returning availabe actions based on card_state and action taken
    #0: stand, 1: hit, 2: doubledown, 3: split
    def possible_actions(self, card_state, action):
        if action == 'initial' or action == 'split':
            if card_state == 'terminal':
                return [0]
            elif len(card_state[0]) == 2 and card_state[0][0] == card_state[0][1]:
                return [0, 1, 2, 3]
            else:
                return [0, 1, 2]
        elif action == 'hit':
            if card_state[0][0] == '21':
                return [0]
            else:
                return [0, 1]

    #Function returning row index Q Matrix for a given card state
    def row_index(self, card_state):

        deck_count = int(self.state.deck_count / len(self.deck.deck) * 300)

        if card_state == 'terminal':
            return (self.state.deck_count+901) * len(self.state.current_states)-1
        else:
            player = card_state[0]
            dealer = card_state[1]
            return (self.state.deck_count+900) * len(self.state.current_states) +\
        len(self.state.dealer_hand) * self.state.player_hand.index(player) + self.state.dealer_hand.index(dealer)

    #Function returning set of possible sums
    def sum_cases(self, hands):
        possible_sums = [0]
        for hand in hands:
            if hand != 'A':
                possible_sums = [case + int(hand) for case in possible_sums]
            else:
                possible_sums = [case + 1 for case in possible_sums] + [case + 11 for case in possible_sums]
        return possible_sums


    #Function returning immediate reward when player stands
    #Q-matrix has to be updated based on the immediate reward
    def stand_reward(self, card_state, dealer_hole):

        #Player's maximum hand total
        player = card_state[0]
        player_totals = [s for s in self.sum_cases(player) if s <= 21]
        player_total = max(player_totals)

        #Dealer's upside down card
        dealer = card_state[1] + (dealer_hole, )
        dealer_total = [s for s in self.sum_cases(dealer) if s <= 21]
        reward = 2 # initialize reward

        #Dealer keeps hitting until going bust
        while dealer_total:

            if max(dealer_total) > player_total: # dealer wins!
                reward = 0
                break

            if max(dealer_total) >= 17:
                if max(dealer_total) == player_total: # draw!
                    reward = 1
                    break
                else:
                    reward = 2 # player wins!
                    break

            #Dealer drawing new card
            add_card = self.deck.draw()
            
            #Dealer updating state
            self.state.update_deck_state(add_card)
            dealer_total = [s for s in self.sum_cases(dealer_total + [add_card]) if s <= 21]


        #Updating Q
        row = self.row_index(card_state)
        next_row = self.row_index('terminal')
        self.Q[row, 0] = (1-self.alpha)*self.Q[row, 0] + self.alpha*(reward+self.gamma*self.Q[next_row, 0])

        return reward

    #Function returning immediate reward when player double downs
    #Q-matrix has to be updated based on the immediate reward    
    def doubledown_reward (self, card_state, dealer_hole):
        player = card_state[0]

        #Player draws new card and updates state 
        add_card = self.deck.draw()
        self.state.update_deck_state(add_card)

        player_totals = [s for s in self.sum_cases(player + (add_card, )) if s <= 21]
        
        #Player busts
        if not player_totals: 
            row = self.row_index(card_state)
            next_row = self.row_index('terminal')
            self.Q[row, 2] = (1-self.alpha)*self.Q[row, 2] + self.alpha*(-1+self.gamma*self.Q[next_row, 0])
            return -1

        #Finding maximum sum of player
        player_total = max(player_totals)
        dealer = card_state[1] + (dealer_hole, )
        dealer_total = [s for s in self.sum_cases(dealer) if s <= 21]
        reward = 3  # initialize a reward

        #Dealer keeps hitting until he goes bust
        while dealer_total:
            if max(dealer_total) > player_total: # dealer wins!
                reward = -1
                break
            
            if max(dealer_total) >= 17:
                if max(dealer_total) == player_total: # draw!
                    reward = 1
                    break
                else:
                    reward = 3 # player wins!
                    break

            #Dealer drawing new card
            add_card = self.deck.draw()
            self.state.update_deck_state(add_card)

            dealer_total = [s for s in self.sum_cases(dealer_total + [add_card]) if s <= 21]

        ## update Q
        row = self.row_index(card_state)
        next_row = self.row_index('terminal')
        self.Q[row, 2] = (1-self.alpha)*self.Q[row, 2] + self.alpha*(reward+self.gamma*self.Q[next_row, 0])

        return reward

    #Function allowing blackjack play and returns profit 
    def blackjack_game(self, card_state=(), dealer_hole=False, phase='initial'):
        if phase == 'initial': # game starts (default)

            #Draw 2 new cards
            player = tuple(self.deck.draw() for _ in range(2))
            dealer = tuple(self.deck.draw() for _ in range(2))

            #Update deck_state
            for p in player:
                self.state.update_deck_state(p)
            for d in dealer:
                self.state.update_deck_state(d)

            #Dealer's face down and hole card 
            dealer_open = dealer[0]
            dealer_hole = dealer[1]

            if set(player) == set(['10', 'A']): # Blackjack!
                return 2.5

            if 'A' in player:
                index_A = player.index('A')
                player = (player[index_A], player[index_A^1])
            elif player[0] != player[1]:
                player = (str(sum([int(p) for p in player])), )
            card_state = (player, (dealer_open, ))

        ## Game continues after the player splits
        elif phase == 'split':
            add_card = self.deck.draw()
            self.state.update_deck_state(add_card)

            ## 'A' exists in the player's hand
            if card_state[0][0] == 'A':
                if add_card == '10':
                    return 2.5
                card_state = (('A', add_card), card_state[1])

            ## 'A' does not exist in the player's hand
            else:
                if add_card == 'A':
                    if card_state[0][0] == '10':
                        return 2.5
                    card_state = (('A', card_state[0][0]), card_state[1])
                else:
                    if card_state[0][0] == add_card:
                        card_state = ((add_card, add_card), card_state[1])
                    else:
                        card_state = ((str(int(add_card)+int(card_state[0][0])), ), card_state[1])

        #Game continues as player keeps on hitting 
        elif phase == 'hit':
            row = self.row_index(card_state)
            add_card = self.deck.draw() #Draw new card 

            #Updating deck and card states 
            self.state.update_deck_state(add_card)
            card_state = self.state.update_card_state(card_state, add_card)
            next_row = self.row_index(card_state)
            if card_state == 'terminal':
                self.Q[row, 1] = (1-self.alpha)*self.Q[row, 1] + self.alpha*(0+self.gamma*self.Q[next_row, 0])
                return 0


            # update Q
            next_actions = self.possible_actions(card_state, phase)
            max_index = 0
            for next_action in next_actions:
                if self.Q[next_row, next_action] > self.Q[next_row, max_index]:
                    max_index = next_action

            self.Q[row, 1] = (1-self.alpha)*self.Q[row, 1] + self.alpha*(0+self.gamma*self.Q[next_row, max_index])

        ## extract possible actions based on card_state and phase
        actions = self.possible_actions(card_state, phase)
        action = np.random.choice(actions)

        #Returning possible states from chossing all possible actions and the dealer's
        #hole card 
        if action == 0: # stand
            return self.stand_reward(card_state, dealer_hole)
        elif action == 1: # hit
            return self.blackjack_game(card_state=card_state, dealer_hole=dealer_hole, phase='hit')
        elif action == 2: # double down
            return self.doubledown_reward (card_state, dealer_hole)
        else: # split
            row = self.row_index(card_state)
            card_state = ((card_state[0][0], ), card_state[1])
            reward1 = self.blackjack_game(card_state=card_state, dealer_hole=dealer_hole, phase='split')
            reward2 = self.blackjack_game(card_state=card_state, dealer_hole=dealer_hole, phase='split')

            ## update Q
            next_row = self.row_index('terminal')
            self.Q[row, 3] = (1-self.alpha)*self.Q[row, 3] + self.alpha*((reward1+reward2)+self.gamma*self.Q[next_row, 0])
            return reward1 + reward2

    #Q-Learn model n times
    def train_rl_agent(self, n):
        for _ in range(n):
            #Dealer uses new card set when remaining cards in deck is less than 40
            if len(self.deck.deck) < 30:
                self.deck = Deck()
                self.deck.shuffle()
                self.state.deck_count = 0
            self.blackjack_game()
