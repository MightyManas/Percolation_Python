import numpy as np
import re
from graphing import graphing_tool as gt

# Your log-power law fit function, for example, a simple power-law
def log_power_law(x, a, b):
    return min(a * 10** (4*b/1.33), a*np.absolute(x-0.5927)**(-b) )

# Function to calculate the average cluster size for a file
def calculate_average_cluster_size(file_path):
    cluster_sizes = []
    
    # Read the data from the file
    with open(file_path, 'r') as f:
        for line in f:
            match = re.search(r'Cluster \d+: Size = (\d+)', line)
            if match:
                cluster_sizes.append(int(match.group(1)))
    
    # Calculate the average cluster size
    if cluster_sizes:
        return np.mean(cluster_sizes)
    else:
        return 0  # In case no valid clusters were found

# Main code for processing files
def process_files():
    avg_cluster_sizes = []
    
    # Loop over the file range
    for i in range(0,12):
        file_path = f"data/data_{i}.txt"
        avg_size = calculate_average_cluster_size(file_path)
        avg_cluster_sizes.append(avg_size)
    
    # Create xdata and ydata for the log-log fit
    xdata = np.absolute(0.585 + np.arange(0,12)*0.001)  # The x-values: file index (1 to 99)
    ydata = np.array(avg_cluster_sizes)  # The y-values: average cluster sizes
    
    # Perform the log transformation
    log_xdata = (xdata)
    log_ydata = (ydata)
    
    # Assuming uncertainties (dy and dx) are known or set to 1
    log_yerr = np.ones_like(log_ydata) * 0.1  # Example error on ydata
    log_xerr = np.ones_like(log_xdata) * 0.001  # Example error on xdata

    # Fit parameters
    p0 = [1, -1]  # Initial guess for the power-law fit (a, b)
    xlabel = r"probability of site occuupation p near $p_c$"
    ylabel = "(Average Cluster Size)"
    title = "Fit of average Cluster Size Distribution"

    # Call the graphing_tool's function to do the fitting and plotting
    a_fit, b_fit, perr = gt(log_power_law, xdata=log_xdata, ydata=log_ydata, dy=log_yerr, dx=log_xerr,
                            p0=p0, xlabel=xlabel, ylabel=ylabel,
                            title=title)
    
    print(f"Fitted parameters: a = {a_fit}, b = {b_fit}")
    print(f"Uncertainties in parameters: {perr}")

# Call the main function
process_files()

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Assume you already have xdata (log L) and ydata (log <s>), 
# or you can prepare them like this:

L = np.array([10000])  # system size (in your case, it's constant)
s_data = np.array([average_cluster_size])  # example: replace with actual average cluster sizes

# Take log of both
log_L = np.log10(L)
log_s = np.log10(s_data)

# Define the linear fit function: log(s) = (gamma/nu) * log(L)
def fit_func(x, slope):
    return slope * x

# Fit the data (assuming you only have a few data points to fit)
params, covariance = curve_fit(fit_func, log_L, log_s)

# Extract the slope, which is gamma/nu
gamma_over_nu = params[0]

# Print result
print(f"Estimated gamma/nu = {gamma_over_nu}")

# Plot the data and the fit
plt.scatter(log_L, log_s, label='Data')
plt.plot(log_L, fit_func(log_L, *params), label=f"Fit: gamma/nu = {gamma_over_nu:.2f}", color='red')
plt.xlabel("log(L)")
plt.ylabel("log(<s>)")
plt.legend()
plt.show()

