import gym
import matplotlib.pyplot as plt
import random
from gym import wrappers
import random

#Calling our environment
environment = gym.make('Blackjack-v0')
environment.reset()

#Setting number of rounds and number to samples from 
num_rounds = 1000 # Payout calculated over num_rounds
num_samples = 1000 # num_rounds simulated over num_samples

average_payoff = []

for sample in range(num_samples):
    round_number = 1
    total_payoff = 0 # to store total payout over 'num_rounds'
    
    while round_number <= num_rounds:
        action = environment.action_space.sample()  # take random action 
        obs, payout, is_done, _ = environment.step(action)
        total_payoff += payout
        
        if is_done:
            environment.reset() # Environment deals new cards to player and dealer
            round_number += 1
    average_payoff.append(total_payoff)

plt.plot(average_payoff, color = "black")                
plt.xlabel('Number of samples')
plt.ylabel('Average payoff after 1000 rounds')
plt.show()    
print ("Average payoff after {} rounds is {}".format(num_rounds, sum(average_payoff)/num_samples))