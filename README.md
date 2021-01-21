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

dict_values([EnvSpec(Copy-v0), EnvSpec(RepeatCopy-v0), EnvSpec(ReversedAddition-v0), EnvSpec(ReversedAddition3-v0), EnvSpec(DuplicatedInput-v0), EnvSpec(Reverse-v0), EnvSpec(CartPole-v0), EnvSpec(CartPole-v1),..... ])
```




