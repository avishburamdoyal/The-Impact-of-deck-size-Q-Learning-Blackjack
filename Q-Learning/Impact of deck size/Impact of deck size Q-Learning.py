import matplotlib.pyplot as plt
import numpy as np

x1 = ['4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21']
y1 = [42.24, 42.59, 42.01, 42.14, 41.13, 41.03, 41.16, 40.37, 40.52, 40.07, 39.81, 38.93, 38.96, 38.36, 38.15, 37.60, 37.81, 37.20]

x2 = ['4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21']
y2 = [41.83, 41.88, 41.95, 42.08, 41.91, 41.53, 41.61, 42.09, 42.37, 41.93, 41.57, 41.77, 41.54, 41.27, 41.38, 41.13, 41.06, 40.85]

x3 = ['4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21']
y3 = [41.45, 41.43, 42.21, 41.90, 42.11, 41.99, 41.67, 42.04, 41.72, 41.40, 42.11, 42.17, 41.21, 41.93, 42.02, 41.50, 41.33, 41.73]

# Set the size of the figure using rcParams
plt.rcParams["figure.figsize"] = (24, 21)  # Increase the width to 10 inches and height to 6 inches

plt.plot(x1, y1, color="black", label='Hi-Lo', linewidth=2)
plt.plot(x2, y2, color="blue", label='Zen-Count', linewidth=2)
plt.plot(x3, y3, color="crimson", label='Uston APC', linewidth=2)
       
plt.legend(loc="upper right", prop={'size': 18})  # Increased font size to 14
#plt.title('Impact of Deck size Q-Learning', fontweight='bold', fontsize=24)
plt.ylabel('Winning odds %', fontsize=30)
plt.xlabel('Deck size', fontsize=30)

# To make the x-axis and y-axis tick numbers bolder and increase tick size
ax = plt.gca()
ax.tick_params(axis='both', which='major', labelsize=18, width=2, length=8)  # Increase tick length to 8

# Save the plot as an image with increased size
plt.savefig('plot_image.png', dpi=300, bbox_inches='tight')

plt.show()

#Zen count vs Uston APC beyond 21 decks 
x_2 = ['4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21', '22', '23', '24', '25', '26', '27', '28', '29', 
       '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44']
y_2 = [41.83, 41.88, 41.95, 42.08, 41.91, 41.53, 41.61, 42.09, 42.37, 41.93, 41.57, 41.77, 41.54, 41.27, 41.38, 41.13, 41.06, 40.85, 40.74, 
       40.47, 40.36, 40.01, 39.97, 39.43, 39.06, 39.92, 39.15, 39.26, 39.14, 39.17, 39.29, 38.70, 38.06, 38.32, 38.27, 38.29, 38.40, 37.09,
       37.48, 37.85, 37.05] 

x_3 = ['4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21', '22', '23', '24', '25', '26', '27', '28', '29', 
       '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44']
y_3 = [41.45, 41.43, 42.21, 41.90, 42.11, 41.99, 41.67, 42.04, 41.72, 41.40, 42.11, 42.17, 41.21, 41.93, 42.02, 41.50, 41.33, 41.73, 41.07, 
       40.55, 40.78, 40.99, 41.02, 40.85, 40.83, 40.32, 41.04, 39.72, 40.15, 39.91, 39.94, 39.99, 39.78, 38.85, 39.30, 39.20, 38.85, 38.71, 
       38.83, 38.90, 38.59] 

# Set the size of the figure using rcParams
plt.rcParams["figure.figsize"] = (24, 21)  # Increase the width to 10 inches and height to 6 inches

plt.plot(x_2, y_2, color="blue", label='Zen-Count', linewidth=2)
plt.plot(x_3, y_3, color="crimson", label='Uston APC', linewidth=2)

plt.legend(loc="upper right", prop={'size': 24})  # Increased font size to 14
#plt.title('Impact of Deck size Q-Learning', fontweight='bold', fontsize=16)
plt.ylabel('Winning odds %', fontsize=30)
plt.xlabel('Deck size', fontsize=30)

# Specify the tick positions and labels to skip every 2 units
tick_positions = np.arange(0, len(x_2), 2)
tick_labels = [x_2[i] for i in tick_positions]
plt.xticks(tick_positions, tick_labels)

# To make the x-axis and y-axis tick numbers bolder and increase tick size
ax = plt.gca()
ax.tick_params(axis='both', which='major', labelsize=15, width=2, length=8)  # Increase tick length to 8

# Increase the font size of the legend
#plt.legend(loc="upper right", prop={'weight':'bold', 'size': 14})  # Increased font size to 14

# Save the plot as an image with increased size
plt.savefig('plot_image.png', dpi=300, bbox_inches='tight')

plt.show()




