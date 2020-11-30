from deck_state import Deck

#Defining state types and updating states based on actions requested
class handState:
    def __init__(self):
        
        #Dealer's hand
        dealer_hand = [(str(i), ) for i in range(2, 11)] + [('A', )]
        self.dealer_hand = dealer_hand

        #Player's hand
        natural_hand = [('A', '10')]
        
        #Hard and soft hands 
        hard_hand = [(str(i), ) for i in range(5, 22)]
        soft_hand = [('A', str(i)) for i in range(2, 10)]
        
        #Pair hands 
        pair_hand = [(str(i), str(i)) for i in range(2, 11)] + [('A', 'A')]
        player_hand = hard_hand + soft_hand + pair_hand
        self.player_hand = player_hand

        #Defining state as a tuple of player's total and dealer's face up 
        current_states = []
        for player in player_hand:
            for dealer in dealer_hand:
                current_states.append((player, dealer))
        current_states += ['terminal']

        self.current_states = current_states

        #Deck states(count)
        self.deck_count = 0

    #Updating deck state based off card counting 
    def update_deck_state(self, add_card):
        
        #Card counting systems 
        
        #Hi-Low system
        #if add_card in ['2', '3', '4', '5', '6']:
            #self.deck_count += 1
        #elif add_card in ['10', 'A']:
            #self.deck_count -= -1
        #elif add_card in ['7','8','9']:
            #self.deck_count -= 0
        
        #Zen count  system
        #if add_card in ['2', '3']:
            #self.deck_count += 1
        #elif add_card in ['4', '5', '6']:
            #self.deck_count -= 2
        #elif add_card in ['7']:
            #self.deck_count -= 1
        #elif add_card in ['8', '9']:
            #self.deck_count -= 0
        #elif add_card in ['10', 'A']:
            #self.deck_count -= -2    
        
        #Uston APC system
        if add_card in ['2', '8']:
            self.deck_count += 1
        elif add_card in ['3', '4', '6', '7']:
            self.deck_count -= 2
        elif add_card in ['5']:
            self.deck_count -= 3
        elif add_card in ['9']:
            self.deck_count -= -1 
        elif add_card in ['10']:
            self.deck_count -= -3 
        elif add_card in ['A']:
            self.deck_count -= 0        
           
    #Possible sums with difference in Ace being treated as '1' or "11"
    def sum_cases(self, hands):
        possible_sums = [0]
        for hand in hands:
            if hand != 'A':
                possible_sums = [case + int(hand) for case in possible_sums]
            else:
                possible_sums = [case + 1 for case in possible_sums] + \
                        [case + 11 for case in possible_sums]
        return possible_sums


    #Updating card states 
    def update_card_state(self, card_state, add_card):
        player = card_state[0]
        dealer = card_state[1]

        ## check if it busts
        is_bust = [s for s in self.sum_cases(player + (add_card, )) if s <= 21]
        if not is_bust:
            return 'terminal'

        # new_card == 'A'
        if add_card == 'A':
            if player == ('A', 'A'):
                return (('A', '2'), dealer)
            elif 'A' in player:
                if player[1] == '10':
                    return (('12', ), dealer)
                elif player[1] == '9':
                    return (('21', ), dealer)
                else:
                    current_sum = int(player[1]) + 1
                    return (('A', str(current_sum)), dealer)
            else:
                current_sum = sum([int(p) for p in player])
                if current_sum >= 20 or current_sum == 10:
                    return (('21', ), dealer)
                if current_sum > 10:
                    return ((str(current_sum+1), ), dealer)
                else:
                    return (('A', str(current_sum)), dealer)

        # new_card != 'A'
        else:
            if player == ('A', 'A'):
                if add_card == '10':
                    return (('12', ), dealer)
                elif add_card == '9':
                    return (('21', ), dealer)
                else:
                    current_sum = int(add_card) + 1
                    return (('A', str(current_sum)), dealer)

            elif 'A' in player:
                current_sum = int(add_card) + int(player[1])
                if current_sum == 10 or current_sum >= 20:
                    return (('21', ), dealer)
                elif current_sum > 10:
                    return ((str(current_sum+1),), dealer)
                else:
                    return (('A', str(current_sum)), dealer)

            else:
                current_sum = sum([int(p) for p in player]) + int(add_card)
                if current_sum == 21:
                    return (('21', ), dealer)
                else:
                    return ((str(current_sum), ), dealer)
