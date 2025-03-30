import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

#reading the data
os.chdir(r'S:\\programing_files\\sem\\Percolation')

for i in range (0,1):

    # Read the file
    with open(f'data_{6000 + i*50}.txt', 'r') as file:
        data = file.read()

    # Extract cluster sizes by splitting the string
    cluster_sizes = data.split(":")[2].strip().split()
    cluster_sizes = [int(size) for size in cluster_sizes]

    cluster_sizes = np.sort(cluster_sizes)
    dict = {}
    for i in cluster_sizes:
        if i in dict:
            dict[i] += 1
        else:
            dict[i] = 1

    #Plot the data
    plt.bar(np.log(np.array(list(dict.keys()))), np.log(np.array(list(dict.values()))))
    plt.xlabel('Cluster Size')  
    plt.ylabel('Frequency')
    plt.title('Cluster Size Distribution')
    plt.grid()
    plt.show()
    #print(dict)
