from graphing import graphing_tool as gt
import numpy as np
import matplotlib.pyplot as plt

# data
data_y = np.array([2.63,2.81,3.01,3.31,3.82,4.30,5.82,6.54,8.70,14.03,24.40,92.10,121.51,127.42,128.08,128.64,128.69,128.89,128.81])
data_x = np.array([0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95])

# function to fit
def f(x,a,b, xi):
    '''    Exponential decay function for curve fitting.'''
    return  a*(np.absolute(xi-x))**(b)

if data_x.shape[0] != data_y.shape[0]:
    raise ValueError("data_x and data_y must have the same shape")
else:
    gt(f,xdata = data_x, ydata = data_y,p0 = [1,4/3,0.595], dy = 0.001, dx = 0.01, title = r'correlation length $\xi$ vs probability', xlabel = 'probability of site occupation', ylabel = 'correlation length')