import re
import numpy as np
from collections import defaultdict
from graphing import graphing_tool as gt

# Step 1: Parse files and build the cluster count matrix
all_counts = []
pattern = re.compile(r"Size\s*=\s*(\d+)")

for i in range(0,12):
    filename = f"data/data_{i}.txt"
    cluster_count = defaultdict(int)
    with open(filename, "r") as file:
        for line in file:
            match = pattern.search(line)
            if match:
                size = int(match.group(1))
                cluster_count[size] += 1
    all_counts.append(cluster_count)

max_size = max(max(d.keys(), default=0) for d in all_counts)
result = np.zeros((12, max_size + 1), dtype=int)

for i, cluster_count in enumerate(all_counts):
    for size, count in cluster_count.items():
        result[i][size] = count

# Step 2: Extract cluster size distribution at p_0
    # Step 4: Define the linear fit function in log-log space
def log_power_law(log_x, log_a, b):
    return log_a + b * log_x

p_0 = 0.58  # Example value for p_0
file_index = int((p_0 - 0.58) / 0.001)

row = result[file_index]
xdata = np.array([s for s, count in enumerate(row) if count > 0])
ydata = np.array([count for count in row if count > 0])

# Step 3: Convert to log-log data
log_xdata = np.log10(xdata)
log_ydata = np.log10(ydata)
log_yerr = 1 / (np.log(10)* np.sqrt(ydata))  # Error propagation for log(y)
log_xerr = np.zeros_like(log_xdata)  # No error in x

# # Define fitting window in actual cluster size s
# smin, smax = 3, 300

# # Get indices for the fitting range
# fit_indices = (xdata >= smin) & (xdata <= smax)

# # Select the data in this range
# x_fit = xdata[fit_indices]
# y_fit = ydata[fit_indices]
# xerr_fit = log_xerr[fit_indices]
# yerr_fit = log_yerr[fit_indices]

# # Take logs
# log_xdata = np.log10(x_fit)
# log_ydata = np.log10(y_fit)
# log_xerr = xerr_fit / (x_fit * np.log(10))  # Propagation of uncertainty
# log_yerr = yerr_fit / (y_fit * np.log(10))


# Step 5: Fit and plot
p0 = [1.0, -2.0]  # Initial guess: log_a ≈ 0, b ≈ -2

xlabel = "log₁₀(Cluster Size s)"
ylabel = "log₁₀(Number of Clusters of Size s)"

gt(log_power_law, xdata=log_xdata, ydata=log_ydata, dy=log_yerr, dx=log_xerr,
p0=p0, xlabel=xlabel, ylabel=ylabel,
title=f"Log-Log Fit of Cluster Size Distribution (p = 0.59274)")

