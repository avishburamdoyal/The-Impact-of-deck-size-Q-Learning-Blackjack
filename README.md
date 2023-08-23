# The Impact of deck-size Q-Learning Blackjack

## Authors 
- Avish Buramdoyal
- Tim Gebbie

## Resources access

- Link: [Paper](https://www.google.com)
- DOI: 


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
The observation space is defined by a 3-tuple of the player's hand total, the dealer's face up card and whether or not the player has a usable ace.

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
The above output shows that the player has no usable ace and a total of 23, i.e. he busted and the dealer's face up is a 3. The player busted by hitting, indicated by **True**. Clearly, the player loses the bet, indicated by -1,

## Generating 3D plots 

To generate the 3D plots from the report,  we make use of the following toolkits: **mpl_toolkits.axes_grid1** and **mpl_toolkits.mplot3D**. 

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
A decaying value of ![epsilon](https://latex.codecogs.com/gif.latex?%5Cepsilon) is used as the exploration factor to ensure the agent minimizes exploring beyond some point where enough about the environment has been learnt. We first set the paramaters of the agent: a Q table, the random exploration factor ![epsilon](https://latex.codecogs.com/gif.latex?%5Cepsilon), the learning rate ![alpha](https://latex.codecogs.com/gif.latex?%5Calpha) and a discount factor, ![gamma](https://latex.codecogs.com/gif.latex?%5Cgamma). ![epsilon](https://latex.codecogs.com/gif.latex?%5Cepsilon) is then reduced linearly as the number of episodes is varied.

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

### Impact of deck-size (Extended Q-Learning: All actions implemented): 
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

In addition, we define a class **Backtest_rl_agent**, based on the training Q model and initialize the required paramaters. We then backtest the model n times and the payoff achieved by the trained agent is returned. 

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

Here, we make use of  3 modules: **main**, **Q Learning - qscores** and **Q Learning - states mapping**. 

Module **main** allows the blackjack simulation to happen. Under the module **Q Learning - qscores**, we use the function **state_conversion** which returns a csv file **Qsa_values.csv** containing action-value entries, **Q(s,a)**. 

```python
def state_conversion(state):
	state = list(state)
	out = ""
	for z in state[:-1]:
		out += str(z) + "-"
	out += str(state[-1])
	return out

with open("q_scores/Qsa_values.csv","w") as file:
	for state, q_values in Q_values.items():
		file.write(state_conversion(state) + ",")
		for q_value in q_values:
			file.write(str(q_value) + ",")
		file.write("\n")
```

The mapping from action-values to states with respective actions is done using a new **state_conversion** function, under the **Q Learning - states** module, calling the **Qsa_values.csv** file and converting it to the strategy table as we require. 

```python
def state_coversion(str):
	out = str.split("-")
	out = [float(k) for k in out]
	out = [int(k) for k in out]
	return tuple(out)

Q_values = defaultdict(lambda: np.zeros(finite_sm.allowable_actions))
with open("q_scores/Qsa_values.csv") as file:
	Q_csv = [line.strip().split(",") for line in file]
for line in Q_csv:
	Q_values[state_coversion(line[0])] = np.array(line[1:-1],dtype=float)
	
actions_possible = {0: "H", 1: "S", 2: "Rh", 3: "DD", 4: "P"}
with open("optimal_policy/Analyzing Strategy Table.csv", "w") as file:
	file.write("state,")
	for dealer in range(2,12):
		file.write(str(dealer) + ",")
	file.write("\n")
	for self_state, actions in policy.items():
		file.write(str(self_state[0]) + " " + str(self_state[1]) + " " + str(self_state[3]) + ",")
		for action in actions:
			file.write(str(actions_possible[action]) + ",")
		file.write("\n")
```

### Perfect card counter implementation: 

In this model, we allow for a variation in the number of players, decks at play and the number of simulations played. We also allow the dealer the choice to either hit or stand on having a soft 17. We choose to make the game more realistic by implementing 4 allowable actions: hit, stand, double down and split. One player, a "perfect card counter" pefectly sizes his bet using the Hi-Lo system and requests actions as per a strategy table. 
 
```python
num_players = eval(input("Enter number of players: ")) 
decks = eval(input("Enter number of decks: ")) 
standOrHit = input("Will the dealer stand or hit on Soft 17: ") 
simulation = eval(input("Enter number of simulations: "))  size

#Deck and ace
deck = [2,3,4,5,6,7,8,9,10,"J","Q","K","A"]*4*decks
ace_value = [1,11]

player_choices = ["hit","double down","stand","split"]
```

We create a function that returns the index to cards based on Hi-Lo system to be used by the perfect card counter to bet at each round. **playersBet** represents an array for which a **random player** randomly chooses one of the 4 entries as % out of bankroll to bet per round. 

```python
def getCount(card):
    if card == 2 or card == 3 or card == 4 or card == 5 or card == 6:
        return 1
    elif card == 7 or card == 8 or card == 9:
        return 0
    else:
        return -1

playersBet = [0.05,0.10,0.35,0.6] 
```

We also have to formulate the **True Count** computation to be stored by the card counter. 

```python
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
            true_count = running_count/decks_remaining
```

We impose intuitive actions for the random player and allow the card counter to follow the basic strategy tables adapted by [[Shackleford, 2019]](http://wizardofodds.com/games/blackjack/strategy/4-decks/)

The random agents always randomly choose an action from **player_choices**. If "hit" is chosen the player hits only 3 times for having a total of less than 6 and hits 2 times for a hand total of 6 or more. This is done to avoid the random agent going a bust. 

```python
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
```

We provide an example of the implementation of the strategy table by [[Shackleford, 2019]](http://wizardofodds.com/games/blackjack/strategy/4-decks/) for the last model. The below example is only for the sake of showing how the strategy table was implemented for one state. The below means that for a case where the dealer stands on soft 17 and the dealer's face up card is a 10, the player will hit for having either a 10 or an ace.

```python
#Dealer stands on soft 17    
if (standOrHit == "stand"):

    if (sum(hands[0])==10):
        if (hands[num_players][0]==10 or hands[num_players][0]=="A"):
            hands[0].append(getValue(deck.pop(0)))
```



