import matplotlib.pyplot as plt
import numpy as np

#1000 simulations, dealer hits on soft 17, 8 decks

y_axis1 = (22.10,14.49,10.73,8.81,7.31)
y_axis2 = (16.91,10.72,8.25,6.84,5.53)
names = ['3','4','5','6','7']


fig = plt.figure(figsize=(24,21), dpi=200)
left, bottom, width, height = 0.1, 0.3, 0.8, 0.6
ax = fig.add_axes([left, bottom, width, height]) 
 
width = 0.15
ticks = np.arange(len(names))    
ax.bar(ticks, y_axis1, width, label='Card counter', color = 'black')
ax.bar(ticks + width, y_axis2, width, align="center",
    label='Random agent', color = 'crimson')

ax.set_ylabel('Average win %', fontsize = 15)
ax.set_xlabel('Number of players', fontsize = 15)
ax.set_xticks(ticks + width/2)
ax.set_xticklabels(names)
#ax.set_title('8 decks, dealer hits on soft 17, 1000 simulations')
ax.legend(bbox_to_anchor =(0.75, 1.15), ncol = 2, prop={'size': 12})
plt.show()

#############################################################################

#1000 simulations, dealer stands on soft 17, 8 decks

y_axis3 = (21.31,14.53,10.89,8.63,8.04)
y_axis4 = (16.58,10.92,8.50,6.65,5.47)
names = ['3','4','5','6','7']


fig = plt.figure(figsize=(24,21), dpi=200)
left, bottom, width, height = 0.1, 0.3, 0.8, 0.6
ax = fig.add_axes([left, bottom, width, height]) 
 
width = 0.15
ticks = np.arange(len(names))    
ax.bar(ticks, y_axis3, width, label='Card counter', color = 'black')
ax.bar(ticks + width, y_axis4, width, align="center",
    label='Random agent', color = 'crimson')

ax.set_ylabel('Average win %', fontsize=15)
ax.set_xlabel('Number of players', fontsize=15)
ax.set_xticks(ticks + width/2)
ax.set_xticklabels(names)
#ax.set_title('8 decks, dealer stands on soft 17, 1000 simulations')

ax.legend(bbox_to_anchor =(0.75, 1.15), ncol = 2, prop={'size': 12})
plt.show()

#############################################################################

#2000 simulations, dealer stands on soft 17, 8 decks

y_axis5 = (21.78,14.74,10.89,8.79,7.20)
y_axis6 = (16.60,11.16,8.46,6.53,5.50)
names = ['3','4','5','6','7']


fig = plt.figure(figsize=(24,21), dpi=200)
left, bottom, width, height = 0.1, 0.3, 0.8, 0.6
ax = fig.add_axes([left, bottom, width, height]) 
 
width = 0.15
ticks = np.arange(len(names))    
ax.bar(ticks, y_axis5, width, label='Card counter', color = 'black')
ax.bar(ticks + width, y_axis6, width, align="center",
    label='Random agent', color = 'crimson')

ax.set_ylabel('Average win %', fontsize=15)
ax.set_xlabel('Number of players', fontsize=15)
ax.set_xticks(ticks + width/2)
ax.set_xticklabels(names)
#ax.set_title('8 decks, dealer stands on soft 17, 2000 simulations')

ax.legend(bbox_to_anchor =(0.75, 1.15), ncol = 2, prop={'size': 12})
plt.show()

