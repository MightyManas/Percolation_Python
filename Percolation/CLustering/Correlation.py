import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
#import seaborn as sns
import os
from graphing import graphing_tool as gt


def f(x,a, xi):
    '''    Exponential decay function for curve fitting.'''
    return  a*np.exp(- x/xi)

os.chdir(r'S:\programing_files\Sem\Percolation\data')
#Create the x and y data points
output_array = np.array([])
y = np.linspace(0.05, 0.95, 19) #probability
for i in range(1,20):
    prob = 0.050000*i
    data = pd.read_csv(f"correlation_length_{prob:.6f}.txt", sep = ' ', header= None)
    x = data[0].values
    z = np.array(data[1].values)
    gt(f,xdata = x,ydata = z,p0 = [1,6], dy = 0.001, dx = 0.01, title = 'correlation function', xlabel = 'distance between two points', ylabel = 'correlation function')

    output_array = np.append(output_array,(z))



    #print(x, y)


x, y = np.meshgrid(x, y)
#print(output_array.shape, output_array)

# Evaluate the function
output_array = output_array.reshape(19,140)
z = output_array

# Plotting
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Surface plot
surf = ax.plot_surface(x, y, z, cmap='viridis')

# Add color bar
fig.colorbar(surf)

# Labels
ax.set_xlabel('Distance bwtween two points')
ax.set_ylabel('Probability')
ax.set_zlabel('Correlation function')
ax.set_title('correlation function of distance between two points and probability')

# Show plot
plt.show()
