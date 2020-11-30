import matplotlib.pyplot as plt
import numpy as np

#1000 simulations, dealer hits on soft 17, 6 players
y_axis1 = (14.77,14.38,14.50,14.33,14.28,14.63,14.36,14.22)
y_axis2 = (11.41,11.28,11.27,11.12,11.10,11.11,10.80,10.98)
names = ['1','2','3','4','5','6','7','8']


fig = plt.figure(figsize=(6,5), dpi=200)
left, bottom, width, height = 0.1, 0.3, 0.8, 0.6
ax = fig.add_axes([left, bottom, width, height]) 
 
width = 0.15
ticks = np.arange(len(names))    
ax.bar(ticks, y_axis1, width, label='Card counter', color = 'black')
ax.bar(ticks + width, y_axis2, width, align="center",
    label='Random agent', color = 'red')

ax.set_ylabel('Average win %', fontsize = 6)
ax.set_xlabel('Number of decks', fontsize = 6)
ax.set_xticks(ticks + width/2)
ax.set_xticklabels(names)
ax.set_title('6 players, dealer hits on soft 17, 1000 simulations')

ax.legend(loc='best', fontsize = 2.5)
plt.show()

#############################################################################

#1000 simulations, dealer stands on soft 17, 6 players

y_axis3 = (14.19,14.52,14.46,14.56,14.47,14.40,14.63,14.63)
y_axis4 = (11.15,11.05,10.71,11.06,11.03,11.07,11.17,11.15)
names = ['1','2','3','4','5','6','7','8']


fig = plt.figure(figsize=(6,5), dpi=200)
left, bottom, width, height = 0.1, 0.3, 0.8, 0.6
ax = fig.add_axes([left, bottom, width, height]) 
 
width = 0.15
ticks = np.arange(len(names))    
ax.bar(ticks, y_axis3, width, label='Card counter', color = 'black')
ax.bar(ticks + width, y_axis4, width, align="center",
    label='Random agent', color = 'red')

ax.set_ylabel('Average win %', fontsize = 6)
ax.set_xlabel('Number of decks', fontsize = 6)
ax.set_xticks(ticks + width/2)
ax.set_xticklabels(names)
ax.set_title('6 players, dealer stands on soft 17, 1000 simulations')

ax.legend(loc='best', fontsize = 2.5)
plt.show()

############################################################################

#2000 simulations, dealer stands on soft 17, 6 players

y_axis5 = (8.69,8.73,8.46,8.63,8.66,8.70,8.72,8.69)
y_axis6 = (6.89,6.65,6.53,6.65,6.60,6.62,6.70,5.59)
names = ['1','2','3','4','5','6','7','8']


fig = plt.figure(figsize=(6,5), dpi=200)
left, bottom, width, height = 0.1, 0.3, 0.8, 0.6
ax = fig.add_axes([left, bottom, width, height]) 
 
width = 0.15
ticks = np.arange(len(names))    
ax.bar(ticks, y_axis5, width, label='Card counter', color = 'black')
ax.bar(ticks + width, y_axis6, width, align="center",
    label='Random agent', color = 'red')

ax.set_ylabel('Average win %', fontsize = 6)
ax.set_xlabel('Number of decks', fontsize = 6)
ax.set_xticks(ticks + width/2)
ax.set_xticklabels(names)
ax.set_title('6 players, dealer hits on soft 17, 2000 simulations')

ax.legend(loc='upper left', fontsize = 2.0)
plt.show()
