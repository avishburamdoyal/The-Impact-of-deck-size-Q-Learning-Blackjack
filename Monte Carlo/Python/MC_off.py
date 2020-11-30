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
    return [1,0] if obs[0]<18 else [0,1]

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
    
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    from mpl_toolkits.mplot3d import Axes3D
    def plot_policy(policy):
    
        def get_Z(player_hand, dealer_showing, usable_ace):
            if (player_hand, dealer_showing, usable_ace) in policy:
                return policy[player_hand, dealer_showing, usable_ace]
            else:
                return 1
    
        def get_figure(usable_ace, ax):
            x_range = np.arange(1, 11)
            y_range = np.arange(11, 22)
            X, Y = np.meshgrid(x_range, y_range)
            Z = np.array([[get_Z(player_hand, dealer_showing, usable_ace) for dealer_showing in x_range] for player_hand in range(21, 10, -1)])
            surf = ax.imshow(Z, cmap=plt.get_cmap('Accent', 2), vmin=0, vmax=1, extent=[0.5, 10.5, 10.5, 21.5])
            plt.xticks(x_range, ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10'))
            plt.yticks(y_range)
            ax.set_xlabel('Player total')
            ax.set_ylabel('Dealer face up card')
            ax.grid(color='black', linestyle='-', linewidth=1)
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="5%", pad=0.1)
            cbar = plt.colorbar(surf, ticks=[0, 1], cax=cax)
            cbar.ax.set_yticklabels(['0 (STICK)','1 (HIT)'])
            cbar.ax.invert_yaxis() 
                
        fig = plt.figure(figsize=(12, 12))
        ax = fig.add_subplot(121)
        ax.set_title('Usable Ace', fontsize=16)
        get_figure(True, ax)
        ax = fig.add_subplot(122)
        ax.set_title('No Usable Ace', fontsize=16)
        get_figure(False, ax)
        plt.show()

def plot_value_function(V, title="Value Function"):
    """
    Plots the value function as a surface plot.
    """
    min_x = min(k[0] for k in V.keys())
    max_x = max(k[0] for k in V.keys())
    min_y = min(k[1] for k in V.keys())
    max_y = max(k[1] for k in V.keys())
        
    x_range = np.arange(min_x, max_x + 1)
    y_range = np.arange(min_y, max_y + 1)
    X, Y = np.meshgrid(x_range, y_range)
        
    # Find value for all (x, y) coordinates
    Z_noace = np.apply_along_axis(lambda _: V[(_[0], _[1], False)], 2, np.dstack([X, Y]))
    Z_ace = np.apply_along_axis(lambda _: V[(_[0], _[1], True)], 2, np.dstack([X, Y]))
        
    def plot_surface(X, Y, Z, title):
        fig = plt.figure(figsize=(16,8))
        ax = fig.add_subplot(111, projection='3d')
        surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                                       cmap=matplotlib.cm.Blues, vmin=-1.0, vmax=1.0)
        ax.set_xlabel('Player total')
        ax.set_ylabel('Dealer face up card')
        ax.set_zlabel('Value')
        ax.set_title(title)
        ax.view_init(ax.elev, -120)
        fig.colorbar(surf)
        plt.show()
        
    plot_surface(X, Y, Z_noace, "{} (No Usable Ace)".format(title))
    plot_surface(X, Y, Z_ace, "{} (Usable Ace)".format(title))

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
#Represents the target policy
def greedy_policy(environment,Q):
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
def MC_offpolicy(environment, episodes, policy, gamma):

        
    # Q is a dictionary that maps state to action values (final action value function)
    Q = defaultdict(lambda: np.zeros(environment.action_space.n))
    
    # The cumulative denominator of the weighted importance sampling formula
    # (across all episodes)
    C = defaultdict(lambda: np.zeros(environment.action_space.n))
        
    #The target policy is the greedy policy we follow 
    target_policy = greedy_policy(environment,Q)
    
    #Printing number of episodes we are one
    for ith_episode in range(1, episodes + 1):
        if ith_episode % 1000 == 0:
            print("\rEpisode {}/{}.".format(ith_episode, episodes), end="")
            clear_output(wait=True)
            
            #Generating an episode which is an array of (state, action, reward) tuples
            episode = []
            environment_state = environment.reset()
            
            for t in range(100):
                # Sample an action from our policy
                prob_policy = target_policy(environment_state) #probability of picking the target policy 
                action = np.random.choice(np.arange(len(prob_policy)), p=prob_policy) #All actions having equal probability of being chose
                next_state, reward, done, _ = environment.step(action) #Environment taking next action after getting into next state
                episode.append((environment_state, action, reward)) #Update all episodes 
                if done:
                    break
                environment_state = next_state  #moving to next state      
                
            # Initializing discounted returns 
            G = 0.0
            
            # Initializing weights of returns for importance sampling ratio
            W = 1.0
            
            # For each step in the episode, backwards
            for t in range(len(episode))[::-1]:
                environment_state, action, reward = episode[t] 
                
                # Update the total reward since step t
                G = gamma * G + reward
                
                # Update weighted importance sampling formula denominator
                C[environment_state][action] += W
                
                # Update the action-value function using the incremental update formula 
                # This also improves our target policy which holds a reference to Q
                Q[environment_state][action] += (W / C[environment_state][action]) * (G - Q[environment_state][action])
                
                # If the action taken by the policy is not the action 
                # taken by the target policy the probability will be 0 and we can break
                if action !=  np.argmax(target_policy(environment_state)):
                    break
                W = W * 1./policy(environment_state)[action]
                        
    return Q, target_policy  

#Calling our environment 
environment = gym.make('Blackjack-v0')
environment.reset()
rand_policy = random_policy(environment.action_space.n)
Q_Pol,Off_MC = MC_offpolicy(environment, 1000000, rand_policy,0.1)

environment.reset()
aver_payoff(environment,1000,1000,Off_MC)

V = defaultdict(float)
for environment_state, actions in Q_Pol.items():
    q_action_value = np.max(actions)
    V[environment_state] = q_action_value
plot_value_function(V, title="Optimal Value Function for Off-Policy Learning")
