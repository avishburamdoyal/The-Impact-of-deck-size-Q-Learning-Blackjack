#Importing classes
import operator
from deck_state import Deck
from env_state import handState
from training import Train_agent

## define the backtest class based on the trained matrix Q
class Backtest_rl_agent:
    ## initialize deck, state, and Q
    def __init__(self, Q):
        self.state= handState()
        self.deck=Deck()
        self.deck.shuffle()
        self.Q=Q

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

        #Dealer keeps hitting until going bust
        while dealer_total:
            if max(dealer_total) > player_total:  # dealer wins!
                return 0

            if max(dealer_total) >= 17:
                if max(dealer_total) == player_total:  # draw!
                    return 1
                else:
                    return 2  # player wins!

            #Dealer drawing new card
            add_card = self.deck.draw()
            self.state.update_deck_state(add_card)
            
            #Dealer updating state
            dealer_total = [s for s in self.sum_cases(dealer_total + [add_card]) if s <= 21]

        return 2

    #Function returning immediate reward when player double downs
    #Q-matrix has to be updated based on the immediate reward
    def doubledown_reward (self, card_state, dealer_hole):
        player = card_state[0]

        #Player drawing a new card and updates state
        add_card = self.deck.draw()
        self.state.update_deck_state(add_card)

        player_totals = [s for s in self.sum_cases(player + (add_card, )) if s <= 21]

        if not player_totals: # player busts
            return -1

        #Finding maximum habd total of player
        player_total = max(player_totals)
        dealer = card_state[1] + (dealer_hole, )
        dealer_total = [s for s in self.sum_cases(dealer) if s <= 21]

        #Dealer keeps hitting until he goes bust
        while dealer_total:
            if max(dealer_total) > player_total:  # dealer wins!
                return -1

            if max(dealer_total) >= 17:
                if max(dealer_total) == player_total:  # draw!
                    return 1
                else:
                    return 3  # player wins!

            #Deler drawing new card and updating state
            add_card = self.deck.draw()
            self.state.update_deck_state(add_card)

            dealer_total = [s for s in self.sum_cases(dealer_total + [add_card]) if s <= 21]

        return 3

    #Function allowing blackjack play and returns profit 
    def blackjack_game(self, card_state=(), dealer_hole=False, phase='initial'):
        if phase == 'initial':  # game starts (default)

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

            if set(player) == set(['10', 'A']):  # Blackjack!
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
            
            #Drawing new card 
            add_card = self.deck.draw()

            #Updating deck and card states
            self.state.update_deck_state(add_card)
            card_state = self.state.update_card_state(card_state, add_card)
            if card_state == 'terminal':
                return 0

        row = self.row_index(card_state)
        actions = self.possible_actions(card_state, phase)
        d = {action: self.Q[row, action] for action in actions}
        action = sorted(d.items(), key=operator.itemgetter(1))[::-1][0][0]
        
        #Returning possible states from chossing all possible actions and the dealer's
        #hole card 
        if action == 0: # stand
            return self.stand_reward(card_state, dealer_hole)
        elif action == 1: # hit
            return self.blackjack_game(card_state=card_state, dealer_hole=dealer_hole, phase='hit')
        elif action == 2: # double down
            return self.doubledown_reward (card_state, dealer_hole)
        else: # split
            card_state = ((card_state[0][0], ), card_state[1])
            return1 = self.blackjack_game(card_state=card_state, dealer_hole=dealer_hole, phase='split')
            return2 = self.blackjack_game(card_state=card_state, dealer_hole=dealer_hole, phase='split')

            return return1 + return2

    #Backtesting model and returning profit for n times
    def backtest_model(self, n):
        profit = [0]
        for _ in range(n):
            if len(self.deck.deck) < 30:
                self.deck=Deck()
                self.deck.shuffle()
                self.state.deck_count = 0
            profit.append(self.blackjack_game())
        return profit
