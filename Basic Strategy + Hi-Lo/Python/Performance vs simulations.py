import random
import matplotlib.pyplot as plt

#Initializing rounds and count 
rounds = 0
true_count = 0
running_count = 0

#Inputs
num_players = eval(input("Enter number of players: ")) #Varying number of players
decks = eval(input("Enter number of decks: ")) #Varying deck size 
standOrHit = input("Will the dealer stand or hit on Soft 17: ") #Allowing dealer to stand or hit on soft 17
simulation = eval(input("Enter number of simulations: ")) #Varying simulation size 

#Deck and ace
deck = [2,3,4,5,6,7,8,9,10,"J","Q","K","A"]*4*decks
ace_value = [1,11]

#Player and dealer: hands,bankroll,bet and actions
table = ""
hands = [[0,0]]*(num_players+1)
bankroll = [0]*(num_players+1)
bet = [0]*(num_players)
player_choices = ["hit","double down","stand","split"] #All actions implemented correctly 

#Player and dealer: wins, losses and draws
wins = [0]*(num_players+1)
losses = [0]*(num_players+1)
draws = [0]*(num_players+1)

#Betting size for random agent 
playersBet = [0.05,0.10,0.35,0.6] #Varying betting size 
cards_dealt = 0
hard = False
randomA = False

#Function that randomizes deck and returns the first card dealt
def getCard():
    random.shuffle(deck)
    first_card = deck.pop(0)
    return first_card

#Function that returns face value of cards 
def getValue(card):
    if card == "J" or card == "Q" or card == "K":
        return  10
    elif card == "A":
        return ace_value[random.randint(0,1)] 
    else:
        return card

#Function that returns index to cards based off Hi-Lo
def getCount(card):
    if card == 2 or card == 3 or card == 4 or card == 5 or card == 6:
        return 1
    elif card == 7 or card == 8 or card == 9:
        return 0
    else:
        return -1
      
#Function returning ace as a 1 for a hard hand           
def getHardA():
    return 1

#Function returning ace as a 11 for a soft hand         
def getSoftA():
    return 11

#Function that indexes first player as card counter, last player as dealer and 
#in between players as random agents
def players():
    for i in range(num_players):
        table[i] = "Player " + str(i)
    table[num_players] = "Dealer"
    
#Minimum and maximum bet set by casino 
minbet = 10
maxbet = 1000

#Initiating casino, random agents and card counter bankroll
casino_bankroll = 100000 #To be updated 
player_bankroll = 1000 #To be updated 
counter_bankroll = 1000 #To be updated [Intial bet based on last true count] 

#Setting counter to iterate over simulation size for dealer, card counter and random agent
sim_count = 0
cardcountersim = [0]*simulation
otherplayersim = [0]*simulation

#Iterating through number of simulations
while (sim_count < simulation):
    deck = [2,3,4,5,6,7,8,9,10,"J","Q","K","A"]*4*decks
    true_count = 0
    if (rounds != 0):
        cardcountersim[sim_count-1] = (wins[0] / rounds) * 100
        otherplayersim[sim_count-1] = (wins[1] / rounds) * 100
    sim_count += 1
    
    #A simulation comes to a halt when we have less than or equal to 25 cards in 
    #the total number of decks used     
    while (len(deck)>25):
        for i in range(1,num_players):
            player_bet = playersBet[random.randint(0,3)]*player_bankroll #Random agent betting randomly based off playersBet array of % 
            bankroll[i] -= player_bet #Updating random agent's bankroll
            bet[i] = player_bet
            hands[i] = [getCard(),getCard()]
            rounds += 1
            hands[i] = [getValue(hands[i][0]),getValue(hands[i][1])]
            
            #Intuitive action for random agent to split
            if ((sum(hands[i]) > 4) and (sum(hands[i]) < 18)):
                if (player_choices[random.randint(0,3)] == 'split'):
                    if hands[i][0] == hands[i][1]:
                        hands[i] = [[hands[i][0],getValue(deck.pop(0))], [hands[i][1],getValue(deck.pop(0))]] 
                        
                        #Random agent doubles down after splitting
                        hands[i][0].append(getValue(deck.pop(0)))
                        hands[i][1].append(getValue(deck.pop(0)))
                        bankroll[i] -= player_bet
                        bet[i] += player_bet
                    else: 
                        
                        #Intuitive action for random agent choosing to hit after splitting
                        if (player_choices[random.randint(0,2)] == 'hit'):
                            
                            #Hit 3 times if sum total less than 6 after splitting
                            if (sum(hands[i])<6):
                                hands[i].append(getValue(deck.pop(0)))
                                hands[i].append(getValue(deck.pop(0)))
                                hands[i].append(getValue(deck.pop(0)))
                            
                            ##Hit 2 times otherwise after splitting
                            else:
                                hands[i].append(getValue(deck.pop(0)))
                                hands[i].append(getValue(deck.pop(0))) 
                                
                                #Player choosing to double down after splitting
                        elif (player_choices[random.randint(0,2)] == 'double down'):
                            hands[i].append(getValue(deck.pop(0)))
                            bankroll[i] -= player_bet
                            bet[i] += player_bet
                        else:
                            
                            #Player choosing to stand after splitting          
                            pass
                        
                #Intuitive action for random agent to hit
                elif (player_choices[random.randint(0,2)] == "hit"): 
                    
                    #Hit 3 times if sum total less than 6
                    if (sum(hands[i])<6):
                        hands[i].append(getValue(deck.pop(0)))
                        hands[i].append(getValue(deck.pop(0)))
                        hands[i].append(getValue(deck.pop(0)))
                    
                    #Hit 2 times if sum total more than or equal to 6
                    else:
                        hands[i].append(getValue(deck.pop(0)))
                        hands[i].append(getValue(deck.pop(0)))
                
                #Intuitive action for random agent to double down
                elif (player_choices[random.randint(0,2)] == 'double down'):
                    hands[i].append(getValue(deck.pop(0)))
                    bankroll[i] -= player_bet
                    bet[i] += player_bet
                else:
                    #do nothing (stand)
                    pass
            else:
                if (sum(hands[i]) == 21):
                    #Player wins
                    pass
                else:
                    #Stand
                    pass
        
        #Dealer
        hands[num_players] = [getCard(),getCard()]
        if "A" in hands[num_players]:
            hands[num_players] = [getValue(hands[num_players][0]),getValue(hands[num_players][1])]
            if (sum(hands[num_players])>=17):
                
                #Dealer chooses to stand on soft 17
                if (standOrHit == "stand"):
                    #do nothing
                    pass
                else:
                    hands[num_players].append(getValue(deck.pop(0)))
                    
            else:
                if (sum(hands[num_players]) <= 15):
                    
                    #Intuitive action for dealer to hit                     
                    if (player_choices[random.randint(0,2)] == 'hit'): 
                        
                            #Hit 3 times if sum total less than 6
                            if (sum(hands[num_players])<6):
                                hands[num_players].append(getValue(deck.pop(0)))
                                hands[num_players].append(getValue(deck.pop(0)))
                                hands[num_players].append(getValue(deck.pop(0)))
                            else:
                                
                                #Hit 2 times if sum total more than or equal to 6
                                hands[num_players].append(getValue(deck.pop(0)))
                                hands[num_players].append(getValue(deck.pop(0)))     
                                
                    #Dealer chooses to double down            
                    elif (player_choices[random.randint(0,2)] == 'double down'):
                        hands[num_players].append(getValue(deck.pop(0)))
                    
                    else:
                        #Dealer chooses to stand      
                        pass
                elif (sum(hands[num_players]) > 21) :
                    print("Busted")     
        hands[num_players] = [getValue(hands[num_players][0]),getValue(hands[num_players][1])]    
        
        #Betting side of card counter (Hi-Lo system)
        bet[0] = 0
        if (rounds == 1):
            bet[0] = 0.05*counter_bankroll
        else:
            if (true_count <3):
                f = 0.00001
            elif (true_count >3 and true_count <5):  #decks_remaining = (decks*52 - cards_dealt)/(decks*52) #true_count = running_count/decks_remaining #Higher the count higher % to bet
                f = 0.15
            elif (true_count >5 or true_count <10):
                f = 0.30
            else:
                f =0.7
        bet[0] = f*counter_bankroll
            
        hands[0] = [getValue(getCard()),getValue(getCard())]
        
        hard = False
        for i in range(len(hands[0])):
            if hands[i] != 11:
                hard = True
        
        #Dealer stands on soft 17 
        if (standOrHit == "stand"):
            #hard
            if (hard):
                for i in range(len(hands[0])):
                    if (hands[0][i] == "A"):
                        hands[0][i] = getHardA()
                    else:
                        hands[0][i] = getValue(hands[0][i])
                    
                while (sum(hands[0]) > 3 and sum(hands[0]) < 9):
                    hands[0].append(getValue(deck.pop(0)))
        
                if (sum(hands[0])== 9):
                    if (sum(hands[num_players])== 3 or sum(hands[num_players])== 4 or sum(hands[num_players])== 5 or sum(hands[num_players])== 6):
                        hands[0].append(getValue(deck.pop(0))) #double down
                        bankroll[0] -= player_bet
                        bet[0] += bet[0]
                        break
                    else:
                        hands[0].append(getValue(deck.pop(0))) #hit
                
                if (sum(hands[0])==10):
                    if (hands[num_players][0]==10 or hands[num_players][0]=="A"):
                        hands[0].append(getValue(deck.pop(0))) #hit
                    else:
                        hands[0].append(getValue(deck.pop(0))) #double down
                        bankroll[0] -= player_bet
                        bet[0] += bet[0]
                        break
        
                if (sum(hands[0])==11):
                    if (hands[num_players][0]=="A"):
                        hands[0].append(getValue(deck.pop(0))) #hit
                    else:
                        hands[0].append(getValue(deck.pop(0))) #double down
                        bankroll[0] -= player_bet
                        bet[0] += bet[0]                        
                        break
        
                if (sum(hands[0])==12):
                    if (hands[num_players][0]== 4 or hands[num_players][0]== 5 or hands[num_players][0]== 6):
                        pass #stand
                    else:
                        hands[0].append(getValue(deck.pop(0))) #hit
            
                if (sum(hands[0])==13 or sum(hands[0])==14 or sum(hands[0])==15 or sum(hands[0])==16):
                    if (hands[num_players][0]== 2 or hands[num_players][0]==3 or hands[num_players][0]==4 or hands[num_players][0]==5 or hands[num_players][0]==6):
                        pass #stand
                    else:
                        hands[0].append(getValue(deck.pop(0))) #hit
                
                if (sum(hands[0]) > 16):
                    pass #stand
            
            #soft 17
            if (hard != True) :
                if (sum(hands[0])==13 or sum(hands[0]) == 14):
                    if (hands[num_players][0]==5 or hands[num_players][0]==6):
                        hands[0].append(getValue(deck.pop(0))) #double down
                        bankroll[0] -= player_bet
                        bet[0] += bet[0]
                        break
                    else:
                        hands[0].append(getValue(deck.pop(0))) #hit
                        
                if (sum(hands[0])==15 or sum(hands[0]) == 16):
                    if (hands[num_players][0]==4 or hands[num_players][0]==5 or hands[num_players][0]==6):
                        hands[0].append(getValue(deck.pop(0))) #double down
                        bankroll[0] -= player_bet
                        bet[0] += bet[0]
                        break
                    else:
                        hands[0].append(getValue(deck.pop(0))) #hit
                        
                if (sum(hands[0]) == 17):
                    if (hands[num_players][0]==3 or hands[num_players][0]==4 or hands[num_players][0]==5 or hands[num_players][0]==6):
                        hands[0].append(getValue(deck.pop(0))) #double down
                        bankroll[0] -= player_bet
                        bet[0] += bet[0]
                        break
                    else:
                        hands[0].append(getValue(deck.pop(0))) #hit
                        
                if (sum(hands[0]) == 18):
                    if (hands[num_players][0]==3 or hands[num_players][0]==4 or hands[num_players][0]==5 or hands[num_players][0]==6):
                        hands[0].append(getValue(deck.pop(0))) #double down
                        bankroll[0] -= player_bet
                        bet[0] += bet[0]
                        break
                    elif (hands[num_players][0]==2 or hands[num_players][0]==7 or hands[num_players][0]==8):
                        pass #stand
                    else:
                        hands[0].append(getValue(deck.pop(0))) #hit
                        
                if (sum(hands[0]) > 18):
                    pass #stand        
            
            #splits
            if (hands[0][0] == hands[0][1]):
                if (hands[0][0] == 2 or hands[0][0] == 3):
                    if (hands[num_players][0]==4 or hands[num_players][0]==5 or hands[num_players][0]==6 or hands[num_players][0]==7): 
                        hands[0] = [[hands[0][0],getValue(deck.pop(0))], [hands[0][1],getValue(deck.pop(0))]] #split
                    else:
                        hands[0].append(getValue(deck.pop(0))) #hit
                        
                if (hands[0][0] == 4): 
                    hands[0].append(getValue(deck.pop(0))) #hit
                
                if (hands[0][0] == 6): 
                    if (hands[num_players][0]==3 or hands[num_players][0]==4 or hands[num_players][0]==5 or hands[num_players][0]==6):   
                        hands[0].append(getValue(deck.pop(0))) #hit
                    else:
                        hands[0] = [[hands[0][0],getValue(deck.pop(0))], [hands[0][1],getValue(deck.pop(0))]] #split        
                
                if (hands[0][0] == 7): 
                    if (hands[num_players][0]==8 or hands[num_players][0]==9 or hands[num_players][0]==10 or hands[num_players][0]=="A"):   
                        hands[0].append(getValue(deck.pop(0))) #hit
                    else:
                        hands[0] = [[hands[0][0],getValue(deck.pop(0))], [hands[0][1],getValue(deck.pop(0))]] #split    
                        
                if (hands[0][0] == 8 or hands[0][0] == 1 or hands[0][0] == 11): 
                    hands[0] = [[hands[0][0],getValue(deck.pop(0))], [hands[0][1],getValue(deck.pop(0))]] #split
                        
                if (hands[0][0] == 9): 
                    if (hands[num_players][0]==7 or hands[num_players][0]==10 or hands[num_players][0]=="A"):
                        pass #stand
                    else:
                        hands[0] = [[hands[0][0],getValue(deck.pop(0))], [hands[0][1],getValue(deck.pop(0))]] #split
        
        else:
            #Dealer hits on soft 17
            for i in range(len(hands[0])):
                if (hands[0][i] == "A"):
                    hands[0][i] = getSoftA()
                else:
                    hands[0][i] = getValue(hands[0][i])
                    
            while (sum(hands[0]) > 3 and sum(hands[0]) < 9):
                hands[0].append(getValue(deck.pop(0)))
                
            if (sum(hands[0])== 9):
                if (sum(hands[num_players])== 3 or sum(hands[num_players])== 4 or sum(hands[num_players])== 5 or sum(hands[num_players])== 6):
                    hands[0].append(getValue(deck.pop(0))) #double down
                    bankroll[0] -= player_bet
                    bet[0] += bet[0]
                    break
                else:
                    hands[0].append(getValue(deck.pop(0))) #hit
                    
            if (sum(hands[0])==10):
                if (hands[num_players][0]==10 or hands[num_players][0]=='A'):
                    hands[0].append(getValue(deck.pop(0))) #hit
                else:
                    hands[0].append(getValue(deck.pop(0))) #double down
                    bankroll[0] -= player_bet
                    bet[0] += bet[0]
                    break
                
            if (sum(hands[0])==11):
                hands[0].append(getValue(deck.pop(0))) #double down
                bankroll[0] -= player_bet
                bet[0] += bet[0]
                break
                
            if (sum(hands[0])==12):
                if (sum(hands[num_players])== 4 or sum(hands[num_players])== 5 or sum(hands[num_players])== 6):
                    pass #stand
                else:
                    hands[0].append(getValue(deck.pop(0))) #hit
                    
            if (sum(hands[0])==13 or sum(hands[0])==14 or sum(hands[0])==15 or sum(hands[0])==16):
                if (sum(hands[num_players])==2 or sum(hands[num_players])==3 or sum(hands[num_players])==4 or sum(hands[num_players])== 5 or sum(hands[num_players])== 6):
                    pass #stand
                else:
                    hands[0].append(getValue(deck.pop(0))) #hit       
            
            if (sum(hands[0]) > 16):
                pass #stand
            
            if (hard != True) :
                if (sum(hands[0])==13 or hands[0] == 14):
                    if (hands[num_players][0]==5 or hands[num_players][0]==6):
                        hands[0].append(getValue(deck.pop(0))) #double down
                        bankroll[0] -= player_bet
                        bet[0] += bet[0]
                        break
                    else:
                        hands[0].append(getValue(deck.pop(0))) #hit
                        
                if (sum(hands[0])==15 or hands[0] == 16):
                    if (hands[num_players][0]==4 or hands[num_players][0]==5 or hands[num_players][0]==6):
                        hands[0].append(getValue(deck.pop(0))) #double down
                        bankroll[0] -= player_bet
                        bet[0] += bet[0]
                        break
                    else:
                        hands[0].append(getValue(deck.pop(0))) #hit
                        
                if (sum(hands[0]) == 17):
                    if (hands[num_players][0]==3 or hands[num_players][0]==4 or hands[num_players][0]==5 or hands[num_players][0]==6):
                        hands[0].append(getValue(deck.pop(0))) #double down
                        bankroll[0] -= player_bet
                        bet[0] += bet[0]
                        break
                    else:
                        hands[0].append(getValue(deck.pop(0))) #hit
                
                if (sum(hands[0]) == 18):
                    if (hands[num_players][0]==2 or hands[num_players][0]==3 or hands[num_players][0]==4 or hands[num_players][0]==5 or hands[num_players][0]==6):
                        hands[0].append(getValue(deck.pop(0))) #double down
                        bankroll[0] -= player_bet
                        bet[0] += bet[0]
                        break
                    elif (hands[num_players][0]==7 or hands[num_players][0]==8):
                        pass #stand
                    else:
                        hands[0].append(getValue(deck.pop(0))) #hit
                        
                if (sum(hands[0]) == 19):
                    if (hands[num_players][0]==6):
                        hands[0].append(getValue(deck.pop(0))) #double down
                        bankroll[0] -= player_bet
                        bet[0] += bet[0]
                        break
                    else:
                        pass #stand
                    
                if (sum(hands[0]) > 19):
                    pass #stand        
            
            #splits
            if ((hands[0][0] == 2 or hands[0][0] == 3) and hands[0][0] == hands[0][1]):
                if (hands[num_players][0]==4 or hands[num_players][0]==5 or hands[num_players][0]==6 or hands[num_players][0]==7):
                    hands[0] = [[hands[0][0],getValue(deck.pop(0))], [hands[0][1],getValue(deck.pop(0))]]  #split 
                else:
                    hands[0].append(getValue(deck.pop(0))) #hit
                    
            if (hands[0][0] == hands[0][1] and hands[0][0] == 4):
                hands[0].append(getValue(deck.pop(0))) #hit
                
            if (hands[0][0] == hands[0][1] and hands[0][0] == 6):
                if (hands[num_players][0]==3 or hands[num_players][0]==4 or hands[num_players][0]==5 or hands[num_players][0]==6):
                    hands[0] = [[hands[0][0],getValue(deck.pop(0))], [hands[0][1],getValue(deck.pop(0))]]  #split 
                else:
                    hands[0].append(getValue(deck.pop(0))) #hit
             
            if (hands[0][0] == hands[0][1] and hands[0][0] == 7):
                if (hands[num_players][0]==8 or hands[num_players][0]==9 or hands[num_players][0]==10 or hands[num_players][0]=='A'):
                    hands[0] = [[hands[0][0],getValue(deck.pop(0))], [hands[0][1],getValue(deck.pop(0))]]  #split 
                else:
                    hands[0].append(getValue(deck.pop(0))) #hit   
                    
            if (hands[0][0] == hands[0][1] and (hands[0][0] == 8 or hands[0][0] == 'A')):
                hands[0] = [[hands[0][0],getValue(deck.pop(0))], [hands[0][1],getValue(deck.pop(0))]]  #split  
                
            if (hands[0][0] == hands[0][1] and hands[0][0] == 9):
                if (hands[num_players][0]==7 or hands[num_players][0]==10 or hands[num_players][0]=='A'):
                    pass #stand 
                else:
                    hands[0] = [[hands[0][0],getValue(deck.pop(0))], [hands[0][1],getValue(deck.pop(0))]]  #split
        
        for i in range(len(hands)):
            for j in range (len(hands[i])):
                if i != (len(hands) - 1):
                    running_count += getCount(hands[i][j])
                    cards_dealt += 1
                else:
                    if j != 1:
                        running_count += getCount(hands[i][j])
                        cards_dealt += 1
                    else:
                        cards_dealt += 1
                        
        decks_remaining = (decks*52 - cards_dealt)/(decks*52)
        if decks_remaining == 0:
            pass
        else:
            true_count = running_count/decks_remaining #Higher the count higher % to bet , i.e. #higher f
                            
        for k in range(num_players):
            if (isinstance(hands[k][0],int)):
                if (sum(hands[num_players])>sum(hands[k]) and sum(hands[num_players]) < 21 and sum(hands[k]) < 21):
                    #dealer wins
                    losses[k] += 1
                    casino_bankroll += bet[k]
                    if k == 0 :
                        wins[num_players] += 1
                elif (sum(hands[num_players])<sum(hands[k]) and sum(hands[num_players]) < 21 and sum(hands[k]) < 21):
                    #player wins
                    wins[k] += 1
                    casino_bankroll -= bet[k]
                    bankroll[k] += 2*bet[k]
                    if k == 0 :
                        losses[num_players] += 1
                elif (sum(hands[num_players])==sum(hands[k]) and sum(hands[num_players]) < 21 and sum(hands[k]) < 21):     
                    #tie
                    draws[k] += 1
                    bankroll[k] += bet[k]
                    if k == 0 :
                        draws[num_players] += 1
                elif (sum(hands[k]) == 21 and len(hands[k]) == 2 and sum(hands[num_players]) == 21 and len(hands[num_players]) == 2):
                    #tie
                    draws[k] += 1
                    bankroll[k] += bet[k]
                    if k == 0 :
                        draws[num_players] += 1
                elif (sum(hands[k]) == 21 and len(hands[k]) == 2 and sum(hands[num_players]) != 21 and len(hands[num_players]) != 2):
                    #player wins
                    wins[k] += 1
                    bankroll[k] += 2.5*bet[k]
                    casino_bankroll -= 1.5*bet[k]
                    
                    if k == 0 :
                        losses[num_players] += 1
                elif (sum(hands[k]) != 21 and len(hands[k]) != 2 and sum(hands[num_players]) == 21 and len(hands[num_players]) == 2):
                    #dealer wins
                    losses[k] += 1
                    casino_bankroll += bet[k]
                    if k == 0 :
                        wins[num_players] += 1
                else: 
                    pass
            else:
                for l in range(0,2):
                    if (sum(hands[num_players])>sum(hands[k][l]) and sum(hands[num_players]) < 21 and sum(hands[k][l]) < 21):
                        #dealer wins
                        losses[k] += 1
                        casino_bankroll += bet[k]                        
                        if k == 0 :
                            wins[num_players] += 1
                    elif (sum(hands[num_players])<sum(hands[k][l]) and sum(hands[num_players]) < 21 and sum(hands[k][l]) < 21):
                        #player wins
                        wins[k] += 1
                        casino_bankroll -= bet[k]
                        bankroll[k] += 2*bet[k]                        
                        if k == 0 :
                            losses[num_players] += 1
                    elif (sum(hands[num_players])==sum(hands[k][l]) and sum(hands[num_players]) < 21 and sum(hands[k][l]) < 21):     
                        #tie
                        draws[k] += 1
                        bankroll[k] += bet[k]
                        if k == 0 :
                            draws[num_players] += 1
                    elif (sum(hands[k][l]) == 21 and len(hands[k][l]) == 2 and sum(hands[num_players]) == 21 and len(hands[num_players]) == 2):
                        #tie
                        draws[k] += 1
                        bankroll[k] += bet[k]
                        if k == 0 :
                            draws[num_players] += 1
                    elif (sum(hands[k][l]) == 21 and len(hands[k][l]) == 2 and sum(hands[num_players]) != 21 and len(hands[num_players]) != 2):
                        #player wins
                        wins[k] += 1
                        bankroll[k] += 2.5*bet[k]
                        casino_bankroll -= 1.5*bet[k]                        
                        if k == 0 :
                            losses[num_players] += 1
                    elif (sum(hands[k][l]) != 21 and len(hands[k][l]) != 2 and sum(hands[num_players]) == 21 and len(hands[num_players]) == 2):
                        #dealer wins
                        losses[k] += 1
                        casino_bankroll += bet[k]
                        if k == 0 :
                            wins[num_players] += 1
                    else:
                        pass              
 
#Dealer and players settlement                
for z in range(num_players+1):
    if z == 0:
        print ('Win percentage for Card Counter: %.2f%%'  % ((wins[z] / rounds) * 100))
        print ('Draw percentage for Card Counter: %.2f%%'  % ((draws[z] / rounds) * 100))    
        print ('Loss percentage for Card Counter: %.2f%%'  % ((losses[z] / rounds) * 100))
        print ("Bankroll of card counter is " + str(bankroll[z]))
    elif (z != num_players):
        print ('Win percentage for Player ' + str(z) + ': %.2f%%' % ((wins[z] / rounds) * 100))
        print ('Draw percentage for Player ' + str(z) + ': %.2f%%' % ((draws[z] / rounds) * 100))
        print ('Loss percentage for Player ' + str(z) + ': %.2f%%' % ((losses[z] / rounds) * 100))
        print ("Bankroll of player " + str(z) + " is " + str(bankroll[z]))
    else: 
        print ('Win percentage for Dealer: %.2f%%' % ((wins[z] / rounds) * 100))
        print ('Draw percentage for Dealer: %.2f%%'  % ((draws[z] / rounds) * 100))    
        print ('Loss percentage for Dealer: %.2f%%' % ((losses[z] / rounds) * 100))
        print ("Bankroll of casino is " + str(casino_bankroll))
       
y_axis = []
x_axis = []
for j in range(simulation-1):
    x_axis.append(j)

#Performance of card counter as a function of number of simulations
for i in range(len(cardcountersim)-1):
    print(cardcountersim[i])
    y_axis.append(cardcountersim[i])
plt.plot(x_axis,y_axis, color = "black", label = 'Card counter')
plt.legend(loc= "upper right")
plt.title('4 players, 7 decks, dealer hits on soft 17, 10000 simulations')
plt.show()
plt.ylabel('Average win %')
plt.xlabel('Number of simulations')

#Performance of other players as a function of number of simulations 
y_axis1 = []
for i in range(len(cardcountersim)-1):
    print(otherplayersim [i])
    y_axis1.append(otherplayersim [i])
plt.plot(x_axis,y_axis1, color = "crimson", label = 'Random agent')
plt.legend(loc= "upper right")
plt.title('4 players, 7 decks, dealer hits on soft 17, 10000 simulations')
plt.show()
plt.ylabel('Average win %')
plt.xlabel('Number of simulations')

#Card counter vs random agent
plt.plot(x_axis,y_axis, color = "black", label = 'Card counter')
plt.plot(x_axis,y_axis1, color = "crimson", label = 'Random agent')
plt.legend(ncol=2, loc='center', bbox_to_anchor=(0.5, 1.06), prop={'size': 24})
#plt.title('5 players, 8 decks, dealer hits on soft 17, 10000 simulations')
plt.ylabel('Average win %', fontsize = 28)
plt.xlabel('Number of simulations', fontsize = 28)
plt.show()

