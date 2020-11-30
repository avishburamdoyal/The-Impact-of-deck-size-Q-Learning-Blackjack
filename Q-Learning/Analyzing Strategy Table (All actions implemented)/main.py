#Libraries and packages
import numpy as np

#Class blackjack simulation
class blackjack_simulation:
	
	def __init__(self):
		
		self.ranges = list(range(4,17)) + list(range(32,38))
		
		# designated range for soft hands
		self.softhands = list(range(32,41))
		self.states = 5
		
		# 0 is hitting, 1 is standing, 2 is surrender, 3 is doubling_down, 4 is splitting
		self.allowable_actions = 5

	def draw(self):
		card = np.random.randint(1,13)
		if card > 10:
			return 10
		return card

	def first_hand(self, hand, add_card):
		if hand == 1: 
			if add_card == 10:
				return 21
			return add_card + 31
		if add_card == 1:
			if hand < 10: 
				return hand + 31
			if hand == 40 or hand == 10:
				return 21
			return hand + 1
		if hand < 21:
			return hand + add_card
		if (hand + add_card) > 41:
			return hand + add_card - 30
		elif (hand + add_card) == 41:
			return 21
		return hand + add_card

	def new_hand(self):
		draw_card = [self.draw() for _ in range(3)]
		self.pair = (draw_card[0] == draw_card[1])
		self.hand = self.first_hand(draw_card[0],draw_card[1])
		
		if draw_card[2] == 1:
			self.dealer = 11
		else:
			self.dealer = draw_card[2] 

		# no point in considering player blackjack
		if self.hand == 21:
			self.hand = self.hand - np.random.randint(1,10)

		self.bet = 1.
		self.terminal = False
		
		# tracks whether this is the first action for doubling down
		self.new = True
		
		# tracks whether we've completed the dealer's hand to get a reward
		self.completed = False

	def actions(self):
		if self.terminal:
			return []
		output = list(range(2))
		if self.new:
			output += [2,3]
			if self.pair:
				output += [4]
		return output

	def clone(self): 
		clone = np.zeros(self.allowable_actions, dtype=int)
		clone[self.actions()] = 1
		return clone

	def clone_for(self, state):
		clone = np.ones(self.allowable_actions, dtype=int)
		if state[2] != 1:
			clone[3] = 0
		if state[3] != 1:
			clone[4] = 0
		return clone

	def hitting(self):
		add_card = self.draw()
		self.hand = self.first_hand(self.hand, add_card)
		if self.hand == 21:
			self.terminal = True
		if self.hand > 21 and self.hand < 31:
			self.bet = -self.bet
			self.terminal = True
		self.new = False
		self.pair = False

	def standing(self):
		self.terminal = True #do nothing

	def surrender(self):
		self.bet = -self.bet / 2
		self.standing()

	def doubling_down(self):
		self.bet *= 2
		self.hitting()
		self.standing()

	def splitting(self):
		if self.hand == 32:
			self.hand = 1
		else:
			self.hand //= 2
		self.bet *= 2
		add_card = self.draw()
		if add_card != self.hand:
			self.pair = False
		self.hand = self.first_hand(self.hand, add_card)
		if self.hand == 21:
			self.terminal = True

	def choose_action(self, action):
		if action == 0:
			self.hitting()
		elif action == 1:
			self.standing()
		elif action == 2:
			self.surrender()
		elif action == 3:
			self.doubling_down()
		elif action == 4:
			self.splitting()
		else:
			return False

	def dealer_total(self):
		add_card = self.draw()
		if (self.dealer == 1 and add_card == 10) or (self.dealer == 10 and add_card == 1):
			self.dealer = 41
			return
		if self.dealer == 11:
			self.dealer = 1
		self.dealer = self.first_hand(self.dealer, add_card)
		while self.dealer in self.ranges:
			add_card = self.draw()
			self.dealer = self.first_hand(self.dealer, add_card)
		self.completed = True

	def settlement(self):
		if not self.terminal:
			return 0
		if self.bet <= 0:
			return self.bet

		if not self.completed:
			self.dealer_total()

		if self.dealer == 41:
			return -1

		if self.hand in self.softhands:
			self.hand -= 20
		if self.dealer in self.softhands:
			self.dealer -= 20
		
		if self.dealer > 21:
			return self.bet
		if self.hand == self.dealer:
			return 0
		if self.hand < self.dealer:
			return -self.bet
		if self.hand > self.dealer:
			return self.bet

	def state(self):
		if self.hand in self.softhands: 
			return tuple(map(int,[self.hand - 20, 1, 1*self.new, 1*self.pair, self.dealer]))
		else:
			return tuple(map(int,[self.hand, 0, 1*self.new, 1*self.pair, self.dealer]))

	def state_format(self,state):
		self.hand = state[0] + 20*state[1]
		self.dealer = state[4]
		self.new = state[2]
		self.pair = state[3]

		self.bet = 1
		self.terminal = False
		self.completed = False

sm = blackjack_simulation()
training_episodes = 1000
averagepayoff_doublingdown = 0
average_reward_hitting = 0
state = (11,0,1,0,4)
for _ in range(training_episodes):
	sm.state_format(state)
	sm.surrender()
	averagepayoff_doublingdown += sm.settlement() / training_episodes
	print(averagepayoff_doublingdown)
	for _ in range(training_episodes):
		sm.state_format(state)
		sm.hitting()
		sm.standing()
		average_reward_hitting += sm.settlement() / training_episodes
		print(average_reward_hitting)