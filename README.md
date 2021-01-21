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

A decaying value of ![epsilon](https://latex.codecogs.com/gif.latex?%5Cepsilon) is used as the exploration factor to ensure the agent minimizes exploring beyond some point where enough about the environment has been learnt. 

