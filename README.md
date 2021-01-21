# The Impact of deck-size Q-Learning Blackjack

## Authors 
-	Avish Buramdoyal
- Tim Gebbie

## Resources access

[link](https://www.google.com)


## Reproducing the research 
All the script files for obtaining the results can be found under [GitHub resource](https://github.com/avb1597/The-Impact-of-deck-size-Q-Learning-Blackjack). The first requirement to reproduce this research is to clone the GitHub resource. Upon the installation of the required packages, the next requirement is to run the script files and produce the results.

## Blackjack Gym Environment 

In the first part of the dissertation, we make use of a blackjack environment "blackjack-v0" provided by OpenGym AI. We first find the available environments.

```python
#Importing gym
import gym
from gym import envs

#Available environments
print(envs.registry.all())

dict_values([EnvSpec(Copy-v0), EnvSpec(RepeatCopy-v0), EnvSpec(ReversedAddition-v0), EnvSpec(ReversedAddition3-v0), 
EnvSpec(DuplicatedInput-v0), EnvSpec(Reverse-v0), EnvSpec(CartPole-v0), EnvSpec(CartPole-v1),..... ])
```

Gym provides a total of 859 environments but we call the blackjack environment.

```python
#Calling environment
environment = gym.make('Blackjack-v0')

environment
<gym.envs.toy_text.blackjack.BlackjackEnv object at 0x000002B617E416A0>
```

## Blackjack Gym environment functionalities 

### State space definition: 
The observation space defined by a 3-tuple of the player's hand total, the dealer's face up card and whether or not the player has a usable ace.

```python
#Verifying state space definition
environment.observation_space
Tuple(Discrete(32), Discrete(11), Discrete(2))
```

The above 3-tuple indicates that there are 32 possible hand totals for the player, 11 possible face up cards for the dealer and 2 possibilities for card ace (1 or 11). 

### Resetting and closing environment: 

By resetting the environment, we get a random state defined by the 3-tuple and actions from the action space can then be performed.

```python
#Resetting environment
environment.reset()
(13, 10, False)

#Closing environment
environment.close()
```
###  Performing an action:

To perform an action, we use the **step** function which takes the **action** as parameter and returns an observation, defined by the 3 tuple.

```python
#Resetting environment and performing a random action
environment.step(environment.action_space.sample())
((23, 3, False), -1.0, True, {})
```
The above output shows that the player has no usable ace and a total of 23, i.e. he busted and the dealer's face up is a 3. The player busted by hitting, indicated by **True***. Clearly, the player loses the bet, indicated by -1,

## Generating 3D plots 

To generate the 3D plots from the report,  we adapt the function from [[Dumke, 2017]](https://github.com/dennybritz/reinforcement-learning/blob/master/lib/plotting.py) and the tutorial by [[Hunter, 2012]](https://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html). The plotting of the value of states required additional toolkits: **mpl_toolkits.axes_grid1** and **mpl_toolkits.mplot3D**. 

## Functions used 

### Monte Carlo Implementation: 

The random policy under MC-off policy is the behaviour policy we follow when generating an episode and takes as argument the number of actions **nA** in the environment and returns a function **policy_function** which returns a vector of probabilities for an observation state.

```python
def random_policy(nA):
    A = np.ones(nA, dtype=float) / nA  
    
    def policy_function(obs):
        return A
    return policy_function
```
We also provide the greedy policy function created for the MC off-policy. The greedy (target) policy, takes as argument the environment and the Q-values and returns the greedy-action policy function. 

```python
def greedy_policy(environment,Q):
    def policy(obs):
        p = np.zeros_like(Q[obs], dtype=float)
        optimal_action = np.argmax(Q[obs])  #get best action by choosing max Q
        p[optimal_action] = 1
        return p
    return policy
```

To allow for learning of states to occur, we make the assumption of exploring starts, making sure that all actions have an equal probability of being selected. We also require that all episodes are updated by the 3 tuple: environment state (player's hand total, dealer's current sum and usable ace or not), action requested and reward achieved.  

```python
prob_policy = target_policy(environment_state)
action = np.random.choice(np.arange(len(prob_policy)), p=prob_policy)
next_state, reward, done, _ = environment.step(action)
episode.append((environment_state, action, reward))
```

### Q-Learning (Hit and Stand only): 
A decaying value of ![epsilon](https://latex.codecogs.com/gif.latex?%5Cepsilon) is used as the exploration factor to ensure the agent minimizes exploring beyond some point where enough about the environment has been learnt. We first set the paramaters of the agent: a Q table, the random exploration factor ![epsilon](https://latex.codecogs.com/gif.latex?%5Cepsilon), the learning rate ![alpha](https://latex.codecogs.com/gif.latex?%5Calpha) and discount factor ![gamma](https://latex.codecogs.com/gif.latex?%5Cgamma). ![epsilon](https://latex.codecogs.com/gif.latex?%5Cepsilon) is then reduced linearly as the number of episodes is varied, as adapted from [[Bija, 2017]](https://github.com/Pradhyo/blackjack/blob/master/blackjack.ipynb)

```python
#Setting paramateres of our RL agent 
self.Q_table = dict()   
self.epsilon = epsilon   
self.alpha = alpha       
self.gamma = gamma       

#Epsilon decay
self.num_training_episodes = num_training_episodes 
self.small_decay = (0.1 * epsilon) / (0.3 * num_training_episodes)         
self.big_decay = (0.8 * epsilon) / (0.4 * num_training_episodes)
self.num_remaining_training_episodes= num_training_episodes
```

The function **paramaters** is created to update epsilon based on the number of training episodes. Also, both ![epsilon](https://latex.codecogs.com/gif.latex?%5Cepsilon) and the learning rate ![alpha](https://latex.codecogs.com/gif.latex?%5Calpha) are set to 0 when no learning happens.

```python
def parameters(self):
    if self.num_remaining_training_episodes > 0.7 *self.num_training_episodes:
        self.epsilon -= self.small_decay
    elif self.num_remaining_training_episodes > 0.3 *self.num_training_episodes:
        self.epsilon -= self.big_decay
    elif self.num_remaining_training_episodes > 0:
        self.epsilon -= self.small_decay
    else:
        self.epsilon = 0.0
        self.alpha = 0.0
    self.num_remaining_training_episodes -= 1
```

### Impact of deck-size Q-Learning Blackjack (Hit and Stand only): 
Here, we allow for a variation in our deck size by defining the class **Deck**. In this case, we are allowing for a blackjack game with 8 decks but the number of decks had to be manually changed to assess the impact a variation in deck size across different counting systems would have. 

```python
class Deck:

#Drawing new deck 
    def __init__(self):
        deck_list = []
        for i in range(2, 10):
            deck_list  += [str(i)] * 4 * 8  # 8-deck Blackjack game
            deck_list  += ['10'] * 16 * 8 + ['A'] * 4 * 8
            self.deck = deck_list 
```

The agent is trained using the Q-Learning algorithm. We define the training parameters ![alpha](https://latex.codecogs.com/gif.latex?%5Calpha), ![gamma](https://latex.codecogs.com/gif.latex?%5Cgamma) and Q. A function **train\_rl\_agent** is then defined to train the agent n times using the Q Learning algorithm. It is also noted that the dealer deals a new card set when the number of cards in the deck is less than 30. 

```python
class Train_agent:
    def __init__(self, alpha, gamma):
        self.alpha = alpha # learning rate
        self.gamma = gamma
        self.state = handState()
        self.deck = Deck()
        self.deck.shuffle()
        self.Q = np.matrix(np.zeros([len(self.state.current_states)*1801, 4]))
    
    def train_rl_agent(self, n):
        for _ in range(n):
            if len(self.deck.deck) < 30:
                self.deck = Deck()
                self.deck.shuffle()
                self.state.deck_count = 0
            self.blackjack_game()
```

In addition, we define a class **Backtest_rl_agent** adapted from [[Jung, 2018]](https://github.com/youngho92/Blackjack_Project-ReinforcementLearning/blob/master/codes/backtest.py) based on the training Q model and initialize the required paramaters. We then backtest the model n times and the payoff achieved by the trained agent is returned. 

```python
class Backtest_rl_agent:
    
    def __init__(self, Q):
        self.state= handState()
        self.deck=Deck()
        self.deck.shuffle()
        self.Q=Q

def backtest_model(self, n):
    profit = [0]
    for _ in range(n):
        if len(self.deck.deck) < 30:
            self.deck=Deck()
            self.deck.shuffle()
            self.state.deck_count = 0
        profit.append(self.blackjack_game())
    return profit
```
### Analyzing Strategy Table (Extended Q-Learning: All actions implemented): 

Here, we adapt the functions from [[Wu, 2018]](https://github.com/nalkpas/CS230-2018-Project) and make use of only 3 modules: **main**, **Q Learning - qscores** and **Q Learning - states mapping**.
