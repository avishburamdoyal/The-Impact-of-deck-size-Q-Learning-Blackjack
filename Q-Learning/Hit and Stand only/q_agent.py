import gym
import matplotlib.pyplot as plt
import random
from gym import wrappers
import random

class RL_Agent():
    def __init__(self, environment, epsilon=1.0, alpha=0.05, gamma=0.1, num_training_episodes=1000):
        self.environment = environment

        #Finding valid number of actions
        self.allowable_actions = list(range(self.environment.action_space.n))

        #Setting paramateres of our RL agent 
        self.Q_table = dict()    # Q-table which will be a dictionary of tuples
        self.epsilon = epsilon   # Random exploration factor
        self.alpha = alpha       # Learning factor
        self.gamma = gamma       # Discount factor- closer to 1 learns well into distant future

        #Epsilon decay
        self.num_training_episodes = num_training_episodes # Change epsilon each episode based on this
        self.small_decay = (0.1 * epsilon) / (0.3 * num_training_episodes) # reduces epsilon slowly
        self.big_decay = (0.8 * epsilon) / (0.4 * num_training_episodes) # reduces epilon faster

        self.num_remaining_training_episodes= num_training_episodes

    #Updating epsilon after each action and set them to 0 if not learning
    def parameters(self):
        
        if self.num_remaining_training_episodes > 0.7 * self.num_training_episodes:
            self.epsilon -= self.small_decay
        elif self.num_remaining_training_episodes > 0.3 * self.num_training_episodes:
            self.epsilon -= self.big_decay
        elif self.num_remaining_training_episodes > 0:
            self.epsilon -= self.small_decay
        else:
            self.epsilon = 0.0
            self.alpha = 0.0

        self.num_remaining_training_episodes -= 1
        
    #Setting initial Q values to 0 if observation not already in Q table
    def Q_for_new_obs(self, observation):
        if observation not in self.Q_table:
            self.Q_table[observation] = dict((action, 0.0) for action in self.allowable_actions)
    
    #Called when agent is asked to find the maximum Q-value of all actions based
    #on the 'observation' of the environment. 
    def max_Q(self, observation):
        
        self.Q_for_new_obs(observation)
        return max(self.Q_table[observation].values())
    
    #Choosing action to take based on observation 
    #Initialize Q values for which observation hasn't been seen to 0.0
    def choose_action(self, observation):
        
        self.Q_for_new_obs(observation)

        # uniformly distributed random number > epsilon happens with probability 1-epsilon
        if random.random() > self.epsilon:
            maxQ = self.max_Q(observation)

            # multiple actions could have maxQ- pick one at random in that case
            # this is also the case when the Q value for this observation were just set to 0.0
            action = random.choice([k for k in self.Q_table[observation].keys()
                                    if self.Q_table[observation][k] == maxQ])
        else:
            action = random.choice(self.allowable_actions)

        self.parameters()

        return action

    #Called after the agent completes an action and receives a reward
    #Function does not consider future rewards while conducting learning
    def learn_state(self, observation, action, reward, next_observation):
        
        self.Q_table[observation][action] += self.alpha * (reward
                                                     + (self.gamma * self.max_Q(next_observation))
                                                     - self.Q_table[observation][action])

import gym
environment = gym.make('Blackjack-v0')
# env = wrappers.Monitor(env, './logs/blackjack-Q', False, True)
import matplotlib.pyplot as plt

q_agent = RL_Agent(environment=environment, epsilon=1.0, alpha=0.05, gamma=0.1, num_training_episodes=1000)

num_rounds = 1000 # Payout calculated over num_rounds
num_samples = 1000 # num_rounds simulated over num_samples

average_payoff = []

observation = environment.reset()
for sample in range(num_samples):
    round_number = 1
    total_payoff = 0 # to store total payout over 'num_rounds'
    # Take action based on Q-table of the agent and learn based on that until 'num_episodes_to_train' = 0
    while round_number <= num_rounds:
        action = q_agent.choose_action(observation)
        next_observation, payout, is_done, _ = environment.step(action)
        q_agent.learn_state(observation, action, payout, next_observation)
        total_payoff += payout
        observation = next_observation
        if is_done:
            observation = environment.reset() # Environment deals new cards to player and dealer
            round_number += 1
    average_payoff.append(total_payoff)

# Plot payout per 1000 episodes for each value of 'sample'
plt.plot(average_payoff, color='k')           
plt.xlabel('Number of samples')
plt.ylabel('Average payoff after 1000 rounds')
plt.show()      
    
print ("Average payout after {} rounds is {}".format(num_rounds, sum(average_payoff)/(num_samples)))