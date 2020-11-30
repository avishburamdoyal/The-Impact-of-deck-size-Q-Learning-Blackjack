#Importing required packages 
import gym
from gym import envs
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
from matplotlib import cm
from collections import defaultdict
from IPython.display import clear_output

#Calling our environment 
environment = gym.make('Blackjack-v0')
num_rounds = 1000

#Simple basic strategy 
def policy_drawtill(obs):
    return [1,0] if obs[0]<19 else [0,1]

#Function that returns average payoff of a player based off 
#our environment, number of rounds player plays agaisnt dealer, 
#number of players in game and policy we follow
def aver_payoff(environment,num_rounds,num_players,policy_used):
    average_payoff = []
    
    for player in range(num_players):
        round_number = 1 #To iterate over round_number
        total_payoff = 0 # to store total payout over 'num_rounds'

        while round_number <= num_rounds:
            action = np.argmax(policy_used(environment._get_obs())) #Returns indices of maximum values
            obs, payout, is_done, _ = environment.step(action) #Takes an action if observation and payout done after round
            if is_done: #observation and payout returned 
                total_payoff += payout #Appending actual payout to total_payoff
                environment.reset() # Environment deals new cards to player and dealer
                round_number += 1
        average_payoff.append(total_payoff)

    plt.plot(average_payoff,  color = "black")                
    plt.xlabel('Number of rounds')
    plt.ylabel('Average payoff after ' + str(num_rounds) + 'rounds')
    plt.show()    
    print ("Average payoff of a player after {} rounds is {}".format(num_rounds, sum(average_payoff)/num_players)) #Average payoff of a player
    
#Initiating a random policy taking as argument number of actions in 
#blackjack environment and returns a function that takes an observation as input 
#and returns a vector of action probabilities 
def random_policy(nA):
    A = np.ones(nA, dtype=float) / nA  
    
    def policy_function(obs):
        return A
    return policy_function

#Creating our greedy action policy taking as argument our environment and 
#the Q values and returning the greedy-action policy function 
#Represents the behaviour policy
def greedy_policy(environment,Q,epsilon):
    def policy(obs):
        p = np.zeros_like(Q[obs], dtype=float)
        optimal_action = np.argmax(Q[obs])  #get best action
        p[optimal_action] = 1
        return p
    return policy

#Monte Carlo Control Off-Policy Control using Weighted Importance Sampling
#Function that takes as argument our environment, number of episodes to sample
#from, policy to follow while generating episodes and discount factor gamma 
#returns a tuple (Q,policy) 
#policy is a function that takes an observation as an argument and returns
#action probabilities (optimal greedy policy).
def TD(environment, episodes, epsilon, alpha, gamma):

        
    # Q is a dictionary that maps state to action values (final action value function)
    Q = defaultdict(lambda: np.zeros(environment.action_space.n))
    
    #The target policy is the greedy policy we follow 
    target_policy = greedy_policy(environment,Q,epsilon)
    
    #Printing number of episodes we are one
    for ith_episode in range(1, episodes + 1):
        if ith_episode % 1000 == 0:
            print("\rEpisode {}/{}.".format(ith_episode, episodes), end="")
            clear_output(wait=True)
            
        current_state = environment.reset()
        while True:
            prob_policy = target_policy(current_state)   #get epsilon greedy policy
            current_action = np.random.choice(np.arange(len(prob_policy)), p=prob_policy)
            next_state,reward,done,_ = environment.step(current_action)
            next_action = np.argmax(Q[next_state])
            td_target = reward + gamma * Q[next_state][next_action]
            td_error = td_target - Q[current_state][current_action]
            Q[current_state][current_action] = Q[current_state][current_action] + alpha * td_error
            if done:
                break
            current_state = next_state
    return Q, target_policy             

#Calling our environment 
environment = gym.make('Blackjack-v0')
environment.reset()
Q_TD,TD = TD(environment, 1000000, 0.05, 0.01, 0.1)

environment.reset()
aver_payoff(environment,1000,1000,TD)


