#Importing classes
from training import Train_agent
from testing import Backtest_rl_agent

#Trainining 6-deck blackjack game with 0.05 learning rate and 0.01 discount
#to keep the agent short sighted
training =Train_agent(0.05, 0.01)
training.train_rl_agent(500000)

#Backtesting the game 10000 times based on the previous training result
backtest = Backtest_rl_agent(training.Q)
average_payoff = backtest.backtest_model(50000)

#Cumulating average payoff
total_payoff = [average_payoff[0]]
for i in range(1, 50000):
    total_payoff.append(total_payoff[i-1] + average_payoff[i])

#Winning odds
winning_odds = [total_payoff[i]/(2*(i+1)) for i in range(50000)]
print("Winning odd is:", winning_odds[-1]) # print winning odds after player 20000 games
