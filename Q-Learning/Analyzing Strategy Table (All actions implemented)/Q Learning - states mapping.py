#Libraries and Packages
import numpy as np
import numpy.ma as ma
import random
from main import blackjack_simulation
from collections import defaultdict
import pdb	

finite_sm = blackjack_simulation()

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

space_list = []
for hand_total in range(4, 21):
	if hand_total > 4:
		space_list.append([hand_total, 0, 1, 0])
	if hand_total > 12: 
		space_list.append([hand_total, 1, 1, 0])
	if hand_total % 2 == 0:
		space_list.append([hand_total, 0, 1, 1])
	if hand_total == 12:
		space_list.append([hand_total, 1, 1, 1])
space_list = sorted(space_list, key=lambda t: (t[3],t[1],t[0]))

policy = defaultdict(list)
for self_state in space_list:
	for dealer in range(2,12):
		state = self_state + [dealer]
		q_scores = Q_values[tuple(state)]
		clone = 1 - finite_sm.clone_for(state)
		cloned_scores = ma.masked_array(q_scores,clone).filled(-16)
		optimal_action  = np.argmax(cloned_scores)

		policy[tuple(self_state)].append(optimal_action )

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

avg_reward = 0
for episode in range(100000):
	finite_sm.new_hand()

	while True:
		q_scores = Q_values[finite_sm.state()]
		clone = 1 - finite_sm.clone()
		cloned_scores = ma.masked_array(q_scores,clone).filled(-16)
		optimal_action  = np.argmax(cloned_scores)
		finite_sm.choose_action(optimal_action )

		if finite_sm.terminal:
			break

	avg_reward += finite_sm.settlement() / 100000
print(avg_reward) 
