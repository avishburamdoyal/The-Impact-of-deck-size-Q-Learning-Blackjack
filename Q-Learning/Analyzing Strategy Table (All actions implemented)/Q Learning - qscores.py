import numpy as np
import numpy.ma as ma
import random
from main import blackjack_simulation
import pdb
from collections import defaultdict

finite_sm = blackjack_simulation()

#Epsilon
initial_eps = 1
ending_eps = 0.05
epsilon_decay = 400000

Q_values = defaultdict(lambda: np.zeros(finite_sm.allowable_actions))
training_episodes = 10000000
epsdecay_frequency = training_episodes - 100000

#Initiating parameters 
gamma = 0.1
alpha = 0.01

counter = 0

def request_action():
	global counter
	
	random_action = np.random.rand()
	epsilon = ending_eps + max((initial_eps - ending_eps) * (1 - np.exp((counter - epsdecay_frequency)/epsilon_decay)), 0)
	
	q_values = Q_values[finite_sm.state()]
	
	clone = 1 - finite_sm.clone()
	cloned_qvalues = ma.masked_array(q_values,clone).filled(-16)
	optimal_action  = np.argmax(cloned_qvalues)

	if random_action > epsilon:
		return optimal_action 
	else:
		actions = finite_sm.actions()
		actions.remove(optimal_action)
		return random.choice(actions)

for _ in range(training_episodes):
	finite_sm.new_hand()
	state = finite_sm.state()

	while not finite_sm.terminal:
		
		action = request_action()
		finite_sm.choose_action(action)

		if not finite_sm.terminal:
			Q_values[state][action] += alpha*(gamma*np.max(Q_values[finite_sm.state()]) - Q_values[state][action])
			state = finite_sm.state()
		else:
			Q_values[state][action] += alpha*(finite_sm.settlement() - Q_values[state][action])

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

