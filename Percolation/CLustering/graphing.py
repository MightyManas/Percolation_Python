import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.optimize import curve_fit as sc
import numpy as np 
import random
from scipy import stats
from sklearn.metrics import r2_score
import pandas as pd
#from shapely.geometry import LineString
'''This Module helps with the graphing of the data and the curve fitting of the data'''
def graphing_tool(f, p0, dy, dx, xdata = [], ydata = [], csv = False,  title = 'curve fit', xlabel = 'x axis', ylabel = 'yaxis',r_squared = True):
    
    """ 
     Feed this function with the following parameters:
        f : function which represent theoritical explanation of the phenomenon
        xdata : x axis data {optional}
        ydata : y axis data {optional}
        dy : error in ydata
        csv : if the data is in csv file {optional}
        p0 : initial guess of the parameter
        title : title of the graph {optional}
        xlabel : x axis label {optional}
        ylabel : y axis label {optional}
      
        """
    

    #creating np array out of measured data
    if True : 
        if len(xdata) != len(ydata) :
            raise ValueError('xdata and ydata must have the same length')
        else :
            xdata = np.array(xdata)
            ydata = np.array(ydata)

    #taking the data from the csv-file    
    if csv != False :
        data = pd.read_excel(csv, sheet_name='Sheet1')

        xdata = data[0]
        xdata = xdata.to_numpy()    
        ydata = data[1]
        ydata = ydata.to_numpy()

    #using libraray to find best fir parameter and plotting right curve fitted
    popt, pcov = sc(f, xdata, ydata,p0, sigma = dy)
   
    # creating data for model curve
    x_data = np.linspace(min(xdata),max(xdata),150, endpoint=True)
    y_data = f(x_data,*popt)

    #error in the parameter
    perr = np.sqrt(np.diag(pcov))
    t = random.choice(['g','b','r'])
    #perr = np.array([f'{i:5.3f}' for i in perr1])
    #popt = np.array([f'{i:5.3f}' for i in popt])

    #r squared value biz
    if r_squared == True:
        
        #calculating r squared
        y2data = f(xdata,*popt) 
        r_squared = "%5.3f"%r2_score(ydata,y2data) 
    
    else :
        r_squared = 0
    
    #plotting model curve
    fig, ax = plt.subplots(figsize=(4.5,4.5))
    ax.plot(x_data,y_data,f'{t}--',label=f'curve fit \n parameter : {popt}  \n error : {perr} \n $R^2$ : {r_squared}')
    
    # plotting measured value xx
    ax.scatter(xdata,ydata,label = "measured value scatter plot")
    ax.errorbar(xdata,ydata, xerr = dx*3, yerr = dy*3, fmt = 'o', label = 'error bar')

    # graph 
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.grid(True)

    #setting the legend outside the graph
    pos = ax.get_position()
    ax.set_position([pos.x0, pos.y0, pos.width * 0.9, pos.height])
    ax.legend(loc='center right', bbox_to_anchor=(1.25, 0.5))

    #showing the graph
    plt.show()


def linear(x,y):
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    plt.plot(x, y, 'o', label='original data')
    xdata = np.linspace(min(x),max(x),150, endpoint=True)
    ydata = slope*xdata + intercept
    plt.plot(xdata, ydata, 'r', label=f'fitted line \n {slope}x + {intercept} \n $R^2$ : {r_value**2}  ')
    plt.legend()
    plt.show()
    
def linecurve(ypoint,xdata,ydata):
    fig,ax = ax.subplots(figsize =(4.5,4.5))

    ### copy curve line y coords and set to a constant
    lines = [ypoint]*(len(ydata))

    #get intersection 
    first_line = LineString(np.column_stack((xdata,ydata)))
    second_line = LineString(np.column_stack((xdata, lines)))
    intersection = first_line.    intersection(second_line)
    ax.plot(*intersection.xy, 'o')


    ax.plot(xdata,ydata, label = f'experimental curve : equivalence point : {intersection.x}')


    # plot hline and vline
    ax.hlines(y=ypoint, xmin=0, xmax=     intersection.x, clip_on= True, color = 'Green')
    ax.vlines(x=intersection.x, ymin = 2.09, ymax= intersection.y, clip_on= True, color = 'Green')

