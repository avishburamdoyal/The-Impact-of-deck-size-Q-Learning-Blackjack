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

from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.mplot3d import Axes3D

#Calling our environment
env = gym.make('Blackjack-v0') 
num_rounds = 1000

#Testing basic strategy
def policy_drawtill(obs):
      return [1,0] if obs[0]<19 else [0,1]

#Function that returns average payoff of a player based off 
#our environment, number of rounds player plays agaisnt dealer, 
#number of players in game and policy we follow
def aver_payoff(environment,num_rounds,num_players,policy_used):
      average_payoff = []
      
      for player in range(num_players):
            round_number = 1
            total_payoff = 0 # to store total payout over 'num_rounds'

            while round_number <= num_rounds:
                  action = np.argmax(policy_used(environment._get_obs()))
                  obs, payout, is_done, _ = environment.step(action)
                  if is_done:
                        total_payoff += payout
                        environment.reset() # Environment deals new cards to player and dealer
                        round_number += 1
            average_payoff.append(total_payoff)

      plt.plot(average_payoff,  color = "black")                
      plt.xlabel('Number of rounds')
      plt.ylabel('Average payoff after' + str(num_rounds) + 'rounds')
      plt.show()    
      print ("Average payout of a player after {} rounds is {}".format(num_rounds, sum(average_payoff)/num_players))

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
                  ax.set_xlabel('Dealer Showing')
                  ax.set_ylabel('Player Hand')
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


#Creating our greedy action policy taking as argument our environment and 
#the Q values and returning the greedy-action policy function 

def greedy_policy(environment,Q,epsilon):
      def policy(obs):
            p = np.ones(environment.action_space.n, dtype=float) * epsilon / environment.action_space.n  #initiate with same prob for all actions
            optimal_action = np.argmax(Q[obs])  #get best action
            p[optimal_action] += (1.0 - epsilon)
            return p
      return policy

def MC_onpolicy(environment, episodes, gamma, epsilon):
    
      # Keeps track of sum and count of returns for each state
      # An array could be used to save all returns but that's memory inefficient.
      # defaultdict used so that the default value is stated if the observation(key) is not found
      returns_sum = defaultdict(float)
      returns_count = defaultdict(float)
        
      # The final action-value function.
      # A nested dictionary that maps state -> (action -> action-value).
      Q = defaultdict(lambda: np.zeros(environment.action_space.n))
        
      # The policy we're following
      target_policy = greedy_policy(environment,Q,epsilon)
        
      for i in range(1, episodes + 1):
            # Print out which episode we're on
            if i% 1000 == 0:
                  print("\rEpisode {}/{}.".format(i, episodes), end="")
                  clear_output(wait=True)
    
            # Generate an episode.
            # An episode is an array of (state, action, reward) tuples
            episode = []
            environment_state = environment.reset()
            
            for t in range(100): 
                  prob_policy = target_policy(environment_state)
                  action = np.random.choice(np.arange(len(prob_policy)), p=prob_policy)
                  next_state, reward, done, _ = environment.step(action)
                  episode.append((environment_state, action, reward))
                  if done:
                        break
                  environment_state = next_state
    
            # Find all (state, action) pairs we've visited in this episode
            # We convert each state to a tuple so that we can use it as a dict key
            
            state_action_in_episode = set([(tuple(x[0]), x[1]) for x in episode])
            for state, action in state_action_in_episode:
                  state_action_pair = (environment_state, action)
                  
                  #First Visit MC:
                  first_visit_MC = next(i for i,x in enumerate(episode)
                                           if x[0] == state and x[1] == action)
                  # Sum up all rewards since the first occurance
                  G = sum([x[2]*(gamma**i) for i,x in enumerate(episode[first_visit_MC:])])
                  
                  # Calculate average return for this state over all sampled episodes
                  returns_sum[state_action_pair] += G
                  returns_count[state_action_pair] += 1.0
                  Q[environment_state][action] = returns_sum[state_action_pair] / returns_count[state_action_pair]
        
      return Q, target_policy

#Calling our environment
environment = gym.make('Blackjack-v0')
environment.reset()
Q_Pol,On_MC = MC_onpolicy(environment, 1000000, 0.1, 0.05)

environment.reset()
aver_payoff(environment,1000,1000,On_MC)

V = defaultdict(float)
for environment_state, actions in Q_Pol.items():
      q_action_value = np.max(actions)
      V[environment_state] = q_action_value
plot_value_function(V, title="Optimal Value Function for On-Policy Learning")



