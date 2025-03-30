import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

#reading the data
os.chdir(r'S:\\programing_files\\sem\\Percolation\\CLustering')
data = pd.read_csv('grid10000.txt', sep = ' ', header = None)

# Plot the heatmap
cmap = sns.color_palette("tab20", as_cmap=True) # 20 distinct colors
plt.figure(figsize=(10, 8))
sns.heatmap(data, cmap=cmap, square=True, cbar=True)

# Customize plot
plt.title('10000x10000 Heatmap')
plt.show()